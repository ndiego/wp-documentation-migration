// Rewrites relative paths in the Markdown so they work on the site, without touching docs/:
//  - links to other .md files (with optional #fragment)  -> Starlight routes
//  - links/images/<video src>/<img src>/poster into docs/assets -> /assets/... (served by
//    the docs-assets integration, so Astro does not try to optimise ~2.5k images)
// Runs as a remark plugin because Astro's unified pipeline only parses raw HTML (rehype-raw)
// after all user rehype plugins, so raw <video> tags are still strings at rehype time either way.
import path from 'node:path';
import { visit } from 'unist-util-visit';
import { DOCS_DIR, ASSETS_DIR, idFromDocsPath, routeFromId } from '../lib/paths.mjs';

const isExternal = (u) => /^([a-z][a-z0-9+.-]*:|\/\/|#|\/)/i.test(u);

export function rewriteUrl(url, filePath, { mdLinks = true } = {}) {
	if (!url || isExternal(url)) return url;
	const m = /^([^?#]*)(\?[^#]*)?(#.*)?$/.exec(url);
	const [, p, query = '', hash = ''] = m;
	if (!p) return url;
	let abs;
	try {
		abs = path.resolve(path.dirname(filePath), decodeURI(p));
	} catch {
		abs = path.resolve(path.dirname(filePath), p);
	}
	if (abs === ASSETS_DIR || abs.startsWith(ASSETS_DIR + path.sep)) {
		return '/assets/' + path.relative(ASSETS_DIR, abs).split(path.sep).map(encodeURIComponent).join('/') + query + hash;
	}
	if (mdLinks && abs.startsWith(DOCS_DIR + path.sep) && /\.md$/i.test(abs)) {
		return routeFromId(idFromDocsPath(path.relative(DOCS_DIR, abs))) + query + hash;
	}
	return url;
}

const ATTR = /\b(src|href|poster)=(["'])([^"']*)\2/gi;

/** @param {{ mdLinks?: boolean }} [options] mdLinks:false only for measuring the baseline */
export default function remarkDocsPaths(options = {}) {
	return (tree, file) => {
		const filePath = file.path;
		if (!filePath || !path.resolve(filePath).startsWith(DOCS_DIR + path.sep)) return;
		visit(tree, (node) => {
			if ((node.type === 'link' || node.type === 'image' || node.type === 'definition') && node.url) {
				node.url = rewriteUrl(node.url, filePath, options);
			} else if (node.type === 'html' && node.value) {
				node.value = node.value.replace(ATTR, (all, attr, q, url) => `${attr}=${q}${rewriteUrl(url, filePath, options)}${q}`);
			}
		});
	};
}
