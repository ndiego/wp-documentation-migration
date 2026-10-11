<?php
/**
 * Plugin Name: HelpHub Spike Importer
 * Description: Spike harness for the wporg-markdown importer. Registers a hierarchical `helphub_doc`
 *              post type and a subclass of WordPressdotorg\Markdown\Importer modelled on
 *              wporg-developer's DevHub_Docs_Importer / DevHub_Block_Editor_Importer (minus the
 *              Block-Editor-specific link rewriting, so we observe the base importer's behaviour).
 *              Adds `wp spike ...` commands and the same cron hooks DevHub registers.
 *
 * Manifest URL: constant HELPHUB_SPIKE_MANIFEST_URL, else option `helphub_spike_manifest_url`,
 * else http://127.0.0.1:8882/manifest.json
 */

use WordPressdotorg\Markdown\Editor;
use WordPressdotorg\Markdown\Importer;

const HELPHUB_SPIKE_POST_TYPE = 'helphub_doc';
const HELPHUB_SPIKE_BASE      = 'documentation';

add_action( 'init', function () {
	register_post_type( HELPHUB_SPIKE_POST_TYPE, array(
		'label'        => 'HelpHub docs (spike)',
		'public'       => true,
		'hierarchical' => true,
		'show_in_rest' => true,
		'has_archive'  => HELPHUB_SPIKE_BASE,
		'rewrite'      => array( 'slug' => HELPHUB_SPIKE_BASE, 'with_front' => false ),
		'supports'     => array( 'title', 'editor', 'excerpt', 'page-attributes', 'custom-fields', 'revisions' ),
	) );
} );

add_action( 'plugins_loaded', function () {
	if ( ! class_exists( Importer::class ) ) {
		return; // wporg-markdown not active.
	}

	class HelpHub_Spike_Importer extends Importer {
		protected static $instance;

		public static function instance() {
			return static::$instance ??= new static();
		}

		protected function get_base() {
			return home_url( HELPHUB_SPIKE_BASE . '/' );
		}

		protected function get_manifest_url() {
			if ( defined( 'HELPHUB_SPIKE_MANIFEST_URL' ) ) {
				return HELPHUB_SPIKE_MANIFEST_URL;
			}
			return get_option( 'helphub_spike_manifest_url', 'http://127.0.0.1:8882/manifest.json' );
		}

		public function get_post_type() {
			return HELPHUB_SPIKE_POST_TYPE;
		}

		public function init() {
			// Same cron wiring as DevHub_Docs_Importer::do_init().
			add_filter( 'cron_schedules', function ( $s ) {
				$s['15_minutes'] ??= array( 'interval' => 900, 'display' => '15 minutes' );
				return $s;
			} );
			add_action( 'helphub_spike_import_manifest', array( $this, 'import_manifest' ) );
			add_action( 'helphub_spike_import_all_markdown', array( $this, 'import_all_markdown' ) );
			add_action( 'init', function () {
				foreach ( array( 'helphub_spike_import_manifest', 'helphub_spike_import_all_markdown' ) as $hook ) {
					if ( ! wp_next_scheduled( $hook ) ) {
						wp_schedule_event( time(), '15_minutes', $hook );
					}
				}
			} );
			( new Editor( $this ) )->init();

			// Proof of concept (off unless option helphub_spike_rewrite_links is set):
			// rewrite relative .md links and relative image paths to absolute URLs.
			add_filter( 'wporg_markdown_after_transform', array( $this, 'rewrite_relative_urls' ), 10, 2 );
		}

		/** @var int Post currently being imported (the filters don't receive it). */
		protected $current_post_id = 0;

		/** @var array|null markdown_source (relative to manifest) => manifest key. */
		protected $source_to_key = null;

		/**
		 * The before/after_transform filters only get ($text, $post_type), so to resolve
		 * relative paths we need to know which file is being processed. Override the
		 * (protected) per-post method to remember it.
		 */
		protected function update_post_from_markdown_source( $post_id ) {
			$this->current_post_id = $post_id;
			$r = parent::update_post_from_markdown_source( $post_id );
			$this->current_post_id = 0;
			return $r;
		}

		protected function source_to_key() {
			if ( null === $this->source_to_key ) {
				$this->source_to_key = array();
				$ids = get_posts( array( 'post_type' => $this->get_post_type(), 'post_status' => 'publish', 'numberposts' => -1, 'fields' => 'ids' ) );
				foreach ( $ids as $id ) {
					$entry = get_post_meta( $id, $this->manifest_entry_meta_key, true );
					if ( ! empty( $entry['markdown_source'] ) ) {
						list( $key ) = $this->get_existing_for_post( get_post( $id ) );
						$this->source_to_key[ $entry['markdown_source'] ] = $key;
					}
				}
			}
			return $this->source_to_key;
		}

		protected static function normalize_path( $path ) {
			$out = array();
			foreach ( explode( '/', $path ) as $seg ) {
				if ( '..' === $seg ) {
					array_pop( $out );
				} elseif ( '' !== $seg && '.' !== $seg ) {
					$out[] = $seg;
				}
			}
			return implode( '/', $out );
		}

		public function rewrite_relative_urls( $html, $post_type ) {
			if ( ! get_option( 'helphub_spike_rewrite_links' ) || $post_type !== $this->get_post_type() || ! $this->current_post_id ) {
				return $html;
			}
			$entry = get_post_meta( $this->current_post_id, $this->manifest_entry_meta_key, true );
			if ( empty( $entry['markdown_source'] ) ) {
				return $html;
			}
			$dir        = dirname( $entry['markdown_source'] );
			$dir        = '.' === $dir ? '' : $dir . '/';
			$map        = $this->source_to_key();
			$asset_base = get_option( 'helphub_spike_asset_base', 'https://example.org/docs-assets/' );

			return preg_replace_callback(
				'#\s(href|src|poster)="(?![a-z][a-z0-9+.-]*:|/|\#)([^"]*)"#i',
				function ( $m ) use ( $dir, $map, $asset_base ) {
					list( $path, $frag ) = array_pad( explode( '#', $m[2], 2 ), 2, null );
					$resolved = self::normalize_path( $dir . $path );
					if ( preg_match( '#\.md$#i', $resolved ) ) {
						if ( isset( $map[ $resolved ] ) ) {
							$url = $this->get_base() . $map[ $resolved ] . '/';
						} else {
							return $m[0]; // Unknown target: leave it (a CI link check should catch this).
						}
					} else {
						$url = $asset_base . $resolved;
					}
					return ' ' . $m[1] . '="' . esc_url( $url . ( $frag ? '#' . $frag : '' ) ) . '"';
				},
				$html
			);
		}
	}

	HelpHub_Spike_Importer::instance()->init();

	// Spike instrumentation: record the kses/user context the import actually runs in
	// (cron vs WP-CLI), and allow forcing a full re-fetch by disabling ETag checks.
	foreach ( array( 'helphub_spike_import_manifest', 'helphub_spike_import_all_markdown' ) as $hook ) {
		add_action( $hook, function () use ( $hook ) {
			$log   = get_option( 'helphub_spike_context_log', array() );
			$log[] = array(
				'hook'                        => $hook,
				'time'                        => gmdate( 'c' ),
				'wp_doing_cron'               => wp_doing_cron(),
				'wp_cli'                      => defined( 'WP_CLI' ) && WP_CLI,
				'user'                        => get_current_user_id(),
				'unfiltered_html'             => current_user_can( 'unfiltered_html' ),
				'content_save_pre_post_kses'  => has_filter( 'content_save_pre', 'wp_filter_post_kses' ),
				'title_save_pre_kses'         => has_filter( 'title_save_pre', 'wp_filter_kses' ),
			);
			update_option( 'helphub_spike_context_log', $log, false );
		}, 1 );
	}
	add_filter( 'wporg_markdown_check_etags', function ( $check ) {
		return get_option( 'helphub_spike_no_etag' ) ? false : $check;
	} );

	if ( defined( 'WP_CLI' ) && WP_CLI ) {
		WP_CLI::add_command( 'spike', 'HelpHub_Spike_CLI' );
	}
}, 20 );

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	class HelpHub_Spike_CLI {
		/** Run import_manifest(). */
		public function manifest() {
			$t = microtime( true );
			$r = HelpHub_Spike_Importer::instance()->import_manifest();
			if ( is_wp_error( $r ) ) {
				WP_CLI::warning( $r->get_error_message() );
			}
			WP_CLI::log( sprintf( 'manifest: %.2fs', microtime( true ) - $t ) );
		}

		/** Run import_all_markdown(). */
		public function markdown() {
			$t = microtime( true );
			HelpHub_Spike_Importer::instance()->import_all_markdown();
			WP_CLI::log( sprintf( 'markdown: %.2fs', microtime( true ) - $t ) );
		}

		/** Print current user + kses state (what applies when cron/CLI imports). */
		public function kses() {
			WP_CLI::log( 'current user id: ' . get_current_user_id() );
			WP_CLI::log( 'unfiltered_html: ' . var_export( current_user_can( 'unfiltered_html' ), true ) );
			WP_CLI::log( 'DISALLOW_UNFILTERED_HTML: ' . var_export( defined( 'DISALLOW_UNFILTERED_HTML' ) && DISALLOW_UNFILTERED_HTML, true ) );
			WP_CLI::log( 'content_save_pre has wp_filter_post_kses: ' . var_export( has_filter( 'content_save_pre', 'wp_filter_post_kses' ), true ) );
			WP_CLI::log( 'is_multisite: ' . var_export( is_multisite(), true ) );
		}

		/**
		 * Dump all imported posts as JSON lines.
		 *
		 * [--content]
		 */
		public function dump( $args, $assoc ) {
			$q = new WP_Query( array(
				'post_type'      => HELPHUB_SPIKE_POST_TYPE,
				'post_status'    => 'any',
				'posts_per_page' => -1,
				'orderby'        => 'ID',
				'order'          => 'ASC',
			) );
			foreach ( $q->posts as $p ) {
				$row = array(
					'ID'            => $p->ID,
					'post_name'     => $p->post_name,
					'post_title'    => $p->post_title,
					'post_parent'   => $p->post_parent,
					'menu_order'    => $p->menu_order,
					'post_status'   => $p->post_status,
					'post_modified' => $p->post_modified,
					'post_excerpt'  => $p->post_excerpt,
					'permalink'     => get_permalink( $p ),
					'source'        => get_post_meta( $p->ID, 'wporg_markdown_source', true ),
					'etag'          => get_post_meta( $p->ID, 'wporg_markdown_etag', true ),
					'len'           => strlen( $p->post_content ),
				);
				if ( ! empty( $assoc['content'] ) ) {
					$row['post_content'] = $p->post_content;
				}
				echo wp_json_encode( $row, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ), "\n";
			}
		}
	}
}
