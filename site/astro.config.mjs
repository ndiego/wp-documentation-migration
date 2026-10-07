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

// Placeholder: set to the real repo once it exists.
// Baseline switch, only used to measure what the link/id plugins fix, e.g.
//   PREVIEW_BASELINE=links,ids npm run build && npm run check-links
// links: don't rewrite .md links; ids: keep Astro's github-slugger heading ids.
const BASELINE = new Set((process.env.PREVIEW_BASELINE ?? '').split(',').filter(Boolean));

const REPO_EDIT_BASE = 'https://github.com/OWNER/REPO/edit/trunk/site/';

export default defineConfig({
	markdown: {
		processor: unified({
			remarkPlugins: [remarkStripFirstH1, remarkGithubAlerts, remarkVideopress, [remarkDocsPaths, { mdLinks: !BASELINE.has('links') }]],
			rehypePlugins: BASELINE.has('ids') ? [] : [rehypeWpHeadingIds],
		}),
	},
	integrations: [
		starlight({
			title: 'WordPress Documentation (preview)',
			customCss: ['./src/styles/custom.css'],
			// entry.filePath is relative to site/ ("../docs/..."); URL resolution normalises the "..".
			editLink: { baseUrl: REPO_EDIT_BASE },
			// Content lives outside src/content/docs, so tell Starlight to run its Markdown
			// transforms (asides, heading anchor links) on it.
			markdown: { processedDirs: ['../docs'] },
			sidebar: buildSidebar(),
			components: {
				PageTitle: './src/components/PageTitle.astro',
			},
		}),
		docsAssets(),
	],
});
