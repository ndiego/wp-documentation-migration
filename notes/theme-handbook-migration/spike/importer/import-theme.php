<?php
use WordPressdotorg\Markdown\Importer;

/**
 * Theme Handbook importer (SPIKE).
 *
 * The Theme Handbook reuses slugs under different parents (templates x4, template-parts,
 * patterns, testing, ... 9 pages), and one public page sits under a non-public parent
 * (theme-security). The base Importer::import_manifest() cannot express either:
 *
 *  1. Its lookup falls back to `existing[ $doc['slug'] ]` / `slug_only[ $doc['slug'] ]`, so
 *     'templates/templates' matches the already-created top-level 'templates' and is
 *     "updated" instead of created. Fixed here: exact path first; slug fallback only when
 *     the slug is unique in the manifest.
 *  2. process_manifest_doc() creates a missing parent recursively but then drops the new
 *     parent ID. Fixed here.
 *  3. Only published posts are considered existing, so a non-public parent would be
 *     re-created on every cron run. Fixed here by also loading private posts, and by
 *     honouring a manifest `status` field (spike-only extension).
 */
class DevHub_Theme_Handbook_Importer extends DevHub_Docs_Importer {
	/**
	 * Slugs that occur more than once in the current manifest.
	 *
	 * @var array
	 */
	protected $duplicate_slugs = array();

	/**
	 * Initializes object.
	 */
	public function init() {
		parent::do_init(
			'theme',
			'themes',
			// SPIKE: local server (see wp-documentation-migration/notes/theme-handbook-migration/spike).
			'http://host.docker.internal:8765/md/manifest.json'
		);

		add_filter( 'handbook_label', array( $this, 'change_handbook_label' ), 10, 2 );
		add_filter( 'wporg_markdown_after_transform', array( $this, 'after_transform' ), 10, 2 );
	}

	/**
	 * Overrides the default handbook label.
	 *
	 * @param string $label     The default label.
	 * @param string $post_type The handbook post type.
	 * @return string
	 */
	public function change_handbook_label( $label, $post_type ) {
		if ( $this->get_post_type() === $post_type ) {
			$label = __( 'Theme Handbook', 'wporg' );
		}

		return $label;
	}

	/**
	 * Shortcodes that are meant to run in this handbook's Markdown (callout boxes).
	 *
	 * @var string[]
	 */
	protected $allowed_shortcodes = array( 'info', 'tip', 'alert', 'tutorial', 'warning' );

	/**
	 * Post-conversion fixes for this handbook's content.
	 *
	 * The pages about media shortcodes mention [audio], [video], [gallery] and [caption]
	 * literally, in prose and in code. The wp-admin version stores them as [[tag]]; Jetpack
	 * passes them through (and decodes &#91;), so do_shortcode() would run them on display.
	 * Escape every registered shortcode as [[tag]], except the callout shortcodes outside code.
	 *
	 * @param string $html      Converted HTML.
	 * @param string $post_type Post type.
	 * @return string
	 */
	public function after_transform( $html, $post_type ) {
		if ( $this->get_post_type() !== $post_type ) {
			return $html;
		}

		$escape = function ( $text, $keep ) {
			return preg_replace_callback(
				'/' . get_shortcode_regex() . '/',
				function ( $s ) use ( $keep ) {
					if ( ( '[' === $s[1] && ']' === $s[6] ) || in_array( $s[2], $keep, true ) ) {
						return $s[0]; // Already escaped, or allowed to run.
					}
					return '[' . $s[0] . ']';
				},
				$text
			);
		};

		// Code blocks: DevHub's Copy / Expand code buttons (js/function-reference.js) only attach to
		// .wp-block-code, which is what the wp-admin pages have. Jetpack emits <pre><code class="language-x">.
		$html = preg_replace_callback(
			'#<pre>\s*<code(?: class="language-([a-z0-9_+-]+)")?>#i',
			function ( $m ) {
				$lang = $m[1] ?? '';
				return $lang
					? '<pre class="wp-block-code"><code lang="' . esc_attr( $lang ) . '" class="language-' . esc_attr( $lang ) . '">'
					: '<pre class="wp-block-code"><code>';
			},
			$html
		);

		// Split into code / non-code segments.
		$parts = preg_split( '#(<(pre|code)\b[^>]*>.*?</\2>)#s', $html, -1, PREG_SPLIT_DELIM_CAPTURE );
		$out   = '';
		for ( $i = 0; $i < count( $parts ); $i++ ) {
			if ( 1 === $i % 3 ) {
				$out .= $escape( $parts[ $i ], array() );
			} elseif ( 0 === $i % 3 ) {
				$out .= $escape( $parts[ $i ], $this->allowed_shortcodes );
			}
		}
		return $out;
	}

	/**
	 * Import the manifest (path-exact variant of Importer::import_manifest()).
	 */
	public function import_manifest() {
		$response = wp_remote_get( $this->get_manifest_url() );
		if ( is_wp_error( $response ) || 200 !== wp_remote_retrieve_response_code( $response ) ) {
			$message = is_wp_error( $response ) ? $response->get_error_message() : 'Non-200 from Markdown source';
			if ( class_exists( 'WP_CLI' ) ) {
				WP_CLI::error( $message );
			}
			return new WP_Error( 'invalid-manifest', $message );
		}
		$manifest = json_decode( wp_remote_retrieve_body( $response ), true );
		if ( ! $manifest ) {
			if ( class_exists( 'WP_CLI' ) ) {
				WP_CLI::error( 'Invalid manifest' );
			}
			return new WP_Error( 'invalid-manifest', 'Manifest did not unfurl properly.' );
		}

		$slug_counts           = array_count_values( wp_list_pluck( $manifest, 'slug' ) );
		$this->duplicate_slugs = array_keys( array_filter( $slug_counts, fn( $c ) => $c > 1 ) );

		$q = new WP_Query( array(
			'post_type'      => $this->get_post_type(),
			'post_status'    => array( 'publish', 'private' ),
			'posts_per_page' => -1,
		) );
		$this->existing              = array();
		$this->existing['slug_only'] = array();
		foreach ( $q->posts as $post ) {
			list( $key, $data ) = $this->get_existing_for_post( $post );
			$this->existing[ $key ] = $data;
			if ( false !== strpos( $key, '/' ) && ! in_array( $post->post_name, $this->duplicate_slugs, true ) ) {
				$this->existing['slug_only'][ $post->post_name ] = $data;
			}
		}

		$created = $updated = 0;
		foreach ( $manifest as $key => $doc ) {
			$existing = $this->find_existing( $key, $doc );
			if ( $existing ) {
				if ( $this->update_post_from_manifest_doc( $existing['post_id'], $doc ) ) {
					$updated++;
				}
				continue;
			}
			if ( $this->process_manifest_doc_by_key( $key, $manifest ) ) {
				$created++;
			}
		}
		if ( class_exists( 'WP_CLI' ) ) {
			WP_CLI::success( "Created {$created} and updated {$updated} handbook pages." );
		}
	}

	/**
	 * Key existing posts by their page path (get_page_uri) rather than by permalink: a
	 * private post's permalink is ?post_type=...&p=ID under WP-CLI, which would never match.
	 *
	 * @param WP_Post $post Post.
	 * @return array 2-tuple of array key and data.
	 */
	protected function get_existing_for_post( WP_Post $post ) {
		return array( get_page_uri( $post ), array( 'post_id' => $post->ID ) );
	}

	/**
	 * Exact path first; the slug fallback (which lets a page move between parents) only for
	 * slugs that are unique in the manifest.
	 */
	protected function find_existing( $key, $doc ) {
		if ( isset( $this->existing[ $key ] ) ) {
			return $this->existing[ $key ];
		}
		if ( 'index' === $key ) {
			return $this->existing[ $this->get_post_type() ] ?? false;
		}
		if ( in_array( $doc['slug'], $this->duplicate_slugs, true ) ) {
			return false;
		}
		return $this->existing['slug_only'][ $doc['slug'] ] ?? $this->existing[ $doc['slug'] ] ?? false;
	}

	/**
	 * Creates a manifest entry, creating its parent first if needed (and keeping the parent ID).
	 */
	protected function process_manifest_doc_by_key( $key, $manifest ) {
		$doc         = $manifest[ $key ];
		$post_parent = null;
		if ( ! empty( $doc['parent'] ) ) {
			$parent = $this->existing[ $doc['parent'] ] ?? false;
			if ( ! $parent && isset( $manifest[ $doc['parent'] ] ) ) {
				$this->process_manifest_doc_by_key( $doc['parent'], $manifest );
				$parent = $this->existing[ $doc['parent'] ] ?? false;
			}
			if ( ! $parent ) {
				return false;
			}
			$post_parent = $parent['post_id'];
		}

		$post = $this->create_post_from_manifest_doc( $doc, $post_parent );
		if ( ! $post ) {
			return false;
		}
		if ( ! empty( $doc['status'] ) && 'publish' !== $doc['status'] ) {
			wp_update_post( array( 'ID' => $post->ID, 'post_status' => $doc['status'] ) );
			$post = get_post( $post->ID );
		}
		list( $k, $data ) = $this->get_existing_for_post( $post );
		$this->existing[ $k ] = $data;
		return true;
	}
}

DevHub_Theme_Handbook_Importer::instance()->init();
