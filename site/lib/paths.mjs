// Shared path helpers: where docs/ lives and how a Markdown file maps to a Starlight route id.
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const SITE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const DOCS_DIR = path.resolve(SITE_DIR, '../docs');
export const ASSETS_DIR = path.join(DOCS_DIR, 'assets');

/**
 * docs-relative file path -> entry id (= URL path without slashes at the ends).
 *   customization/block-editor/blocks-list.md -> customization/block-editor/blocks-list
 *   customization/README.md                    -> customization
 *   README.md                                  -> index   (Starlight maps "index" to "/")
 */
export function idFromDocsPath(rel) {
	const p = rel.split(path.sep).join('/').replace(/\.md$/i, '');
	if (/(^|\/)readme$/i.test(p)) {
		const dir = p.replace(/\/?readme$/i, '');
		return dir === '' ? 'index' : dir.toLowerCase();
	}
	return p.toLowerCase();
}

/** entry id -> site URL path */
export function routeFromId(id) {
	return id === 'index' || id === '' ? '/' : `/${id}/`;
}
