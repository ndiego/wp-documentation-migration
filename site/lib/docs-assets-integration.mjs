// Serves docs/assets at /assets without copying the ~1.8 GB tree.
//  - dev:   Vite middleware (sirv, supports Range requests so <video> can seek)
//  - build: dist/assets becomes a symlink to docs/assets (for `astro preview`, the link
//           checker, or any static server that follows symlinks)
//  - build with DOCS_ASSETS=copy: dist/assets/images is a real copy of docs/assets/images
//           (~400 MB; videos are NOT copied, the Markdown links to wordpress.org for those).
//           Use this for hosts that upload files, e.g. `npm run build:publish` for Spacefast.
// We deliberately do NOT put a symlink in public/: Astro copies public/ into dist/ on
// build, which would duplicate all videos.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sirv from 'sirv';
import { ASSETS_DIR } from './paths.mjs';

export default function docsAssets() {
	const serve = () => {
		const handler = sirv(ASSETS_DIR, { dev: true, etag: true });
		return (req, res, next) => {
			if (!req.url?.startsWith('/assets/')) return next();
			req.url = req.url.slice('/assets'.length);
			handler(req, res, () => {
				req.url = '/assets' + req.url;
				next();
			});
		};
	};
	return {
		name: 'docs-assets',
		hooks: {
			'astro:server:setup': ({ server }) => {
				server.middlewares.use(serve());
			},
			'astro:build:done': ({ dir, logger }) => {
				const target = path.join(fileURLToPath(dir), 'assets');
				fs.rmSync(target, { recursive: true, force: true });
				if (process.env.DOCS_ASSETS === 'copy') {
					fs.mkdirSync(target, { recursive: true });
					fs.cpSync(path.join(ASSETS_DIR, 'images'), path.join(target, 'images'), { recursive: true });
					logger.info(`copied ${path.join(ASSETS_DIR, 'images')} -> ${target}/images (videos skipped)`);
				} else {
					fs.symlinkSync(path.relative(path.dirname(target), ASSETS_DIR), target, 'dir');
					logger.info(`linked ${target} -> ${ASSETS_DIR}`);
				}
			},
		},
	};
}
