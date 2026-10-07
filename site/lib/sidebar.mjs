// Builds the Starlight sidebar from docs/manifest.json (wporg importer format).
// The manifest is itself generated from the folder tree, so this is the folder tree
// with the importer's `order` applied. Keys are docs paths without extension; folder
// index pages (README.md) have the folder path as key.
import fs from 'node:fs';
import path from 'node:path';
import { DOCS_DIR, idFromDocsPath } from './paths.mjs';

const HIDDEN_LAST = new Set(['uncategorized']);

export function buildSidebar() {
	const manifest = JSON.parse(fs.readFileSync(path.join(DOCS_DIR, 'manifest.json'), 'utf8'));
	const entries = Object.entries(manifest).map(([key, e]) => ({
		key,
		...e,
		id: idFromDocsPath(e.markdown_source),
		isIndex: /(^|\/)README\.md$/i.test(e.markdown_source),
	}));
	const missing = entries.filter((e) => !fs.existsSync(path.join(DOCS_DIR, e.markdown_source)));
	if (missing.length) console.warn(`[sidebar] ${missing.length} manifest entries without a file:`, missing.map((e) => e.key));

	const children = new Map();
	for (const e of entries) {
		const parent = e.parent ?? '';
		if (!children.has(parent)) children.set(parent, []);
		children.get(parent).push(e);
	}
	const sorted = (list) => [...(list ?? [])].sort((a, b) => (a.order ?? 0) - (b.order ?? 0));

	const toItem = (e, depth) => {
		if (!e.isIndex) return { slug: e.id };
		return {
			label: e.title,
			collapsed: depth > 0,
			items: [{ label: 'Overview', slug: e.id }, ...sorted(children.get(e.key)).map((c) => toItem(c, depth + 1))],
		};
	};

	const top = sorted(children.get(''));
	const groups = top.filter((e) => e.isIndex && !HIDDEN_LAST.has(e.key)).map((e) => toItem(e, 0));
	const loosePages = top.filter((e) => !e.isIndex).map((e) => ({ slug: e.id }));
	const tail = top.filter((e) => HIDDEN_LAST.has(e.key)).map((e) => ({ ...toItem(e, 1), collapsed: true }));
	return [
		...groups,
		{ label: 'Other pages', collapsed: true, items: [...loosePages, ...tail] },
	];
}
