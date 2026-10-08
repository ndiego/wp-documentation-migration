// @ts-check
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
// Importing paths.mjs here also records the site folder for bundled code (see SITE_DIR there).
import './lib/paths.mjs';

// Baseline switch, only used to measure what the link/id plugins fix, e.g.
//   PREVIEW_BASELINE=links,ids npm run build && npm run check-links
// links: don't rewrite .md links; ids: keep Astro's github-slugger heading ids.
const BASELINE = new Set((process.env.PREVIEW_BASELINE ?? '').split(',').filter(Boolean));


export default defineConfig({
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
			editLink: { baseUrl: 'https://github.com/ndiego/wp-documentation-migration/edit/restructure/site/' },
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
