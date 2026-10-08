// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
// Astro 7's default Markdown processor (Sätteri) does not run remark/rehype plugins,
// so we opt back into the unified pipeline.
import { unified } from '@astrojs/markdown-remark';

import remarkStripFirstH1 from './plugins/remark-strip-first-h1.mjs';
import remarkGithubAlerts from './plugins/remark-github-alerts.mjs';
import remarkDocsPaths from './plugins/remark-docs-paths.mjs';
import remarkVideopress from './plugins/remark-videopress.mjs';
import rehypeWpHeadingIds from './plugins/rehype-wp-heading-ids.mjs';
import docsAssets from './lib/docs-assets-integration.mjs';
import { buildSidebar } from './lib/sidebar.mjs';

// Baseline switch, only used to measure what the link/id plugins fix, e.g.
//   PREVIEW_BASELINE=links,ids npm run build && npm run check-links
// links: don't rewrite .md links; ids: keep Astro's github-slugger heading ids.
const BASELINE = new Set((process.env.PREVIEW_BASELINE ?? '').split(',').filter(Boolean));


export default defineConfig({
	vite: {
		resolve: {
			// Bundled code (pages, components, routeData.ts) takes the site folder from Astro's own
			// config instead of import.meta.url, which points into dist/ once bundled (lib/site-root.mjs).
			alias: { '#site-root': fileURLToPath(new URL('./lib/site-root.server.mjs', import.meta.url)) },
		},
		server: {
			// content.config.ts globs from the repo root; keep the dev watcher out of the big
			// generated/raw folders (~1.7 GB). data/ is still read at build time, just not watched.
			watch: {
				ignored: [
					'**/.venv/**',
					'**/raw/**',
					'**/docs/assets/**',
					'**/build/before/assets/**',
					'**/notes/**',
					'**/data/**',
					'**/site/dist/**',
				],
			},
		},
	},
	markdown: {
		processor: unified({
			remarkPlugins: [remarkStripFirstH1, remarkGithubAlerts, remarkVideopress, [remarkDocsPaths, { mdLinks: !BASELINE.has('links') }]],
			rehypePlugins: BASELINE.has('ids') ? [] : [rehypeWpHeadingIds],
		}),
	},
	integrations: [
		starlight({
			title: 'WordPress Documentation (structure preview)',
			customCss: ['./src/styles/custom.css'],
			// Needed so Starlight computes an editUrl at all; src/routeData.ts replaces it per tree
			// (proposed: edit on the restructure branch, current: read-only blob at before-restructure).
			editLink: { baseUrl: 'https://github.com/ndiego/wp-documentation-migration/edit/trunk/site/' },
			// Content lives outside src/content/docs, so tell Starlight to run its Markdown
			// transforms (asides, heading anchor links) on it.
			markdown: { processedDirs: ['../docs', '../build/before'] },
			// One top-level group per tree; routeData.ts shows only the current page's tree.
			sidebar: buildSidebar(),
			routeMiddleware: './src/routeData.ts',
			components: {
				PageTitle: './src/components/PageTitle.astro',
				Banner: './src/components/Banner.astro',
				SiteTitle: './src/components/SiteTitle.astro',
				EditLink: './src/components/EditLink.astro',
			},
		}),
		docsAssets(),
	],
});
