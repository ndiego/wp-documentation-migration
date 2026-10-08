// Builds the Starlight sidebar from each tree's manifest.json (wporg importer format).
// The manifest is itself generated from the folder tree, so this is the folder tree
// with the importer's `order` applied. Keys are tree paths without extension; folder
// index pages (README.md) have the folder path as key.
//
// Starlight has a single sidebar config, so it gets one top-level group per tree
// (labels = tree keys). src/routeData.ts then replaces the sidebar on every page with
// the entries of the group that matches the page's tree, so each tree only ever shows
// its own navigation (and prev/next stays inside the tree).
import fs from 'node:fs';
import path from 'node:path';
import { TREES, treeId } from './paths.mjs';

const HIDDEN_LAST = new Set(['uncategorized']);

/** Manifest of one tree as a parent -> sorted children model (also used by the compare page). */
export function loadTree(tree) {
	const manifest = JSON.parse(fs.readFileSync(path.join(tree.dir, 'manifest.json'), 'utf8'));
	const entries = Object.entries(manifest).map(([key, e]) => ({
		key,
		...e,
		id: treeId(tree, e.markdown_source),
		isIndex: /(^|\/)README\.md$/i.test(e.markdown_source),
	}));
	const missing = entries.filter((e) => !fs.existsSync(path.join(tree.dir, e.markdown_source)));
	if (missing.length) console.warn(`[sidebar] ${tree.key}: ${missing.length} manifest entries without a file:`, missing.map((e) => e.key));

	const children = new Map();
	for (const e of entries) {
		const parent = e.parent ?? '';
		if (!children.has(parent)) children.set(parent, []);
		children.get(parent).push(e);
	}
	for (const list of children.values()) list.sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
	return { entries, children, childrenOf: (key) => children.get(key) ?? [] };
}

function treeSidebar(tree) {
	const { childrenOf } = loadTree(tree);
	const toItem = (e, depth) => {
		if (!e.isIndex) return { slug: e.id };
		return {
			label: e.title,
			collapsed: depth > 0,
			items: [{ label: 'Overview', slug: e.id }, ...childrenOf(e.key).map((c) => toItem(c, depth + 1))],
		};
	};
	const top = childrenOf('');
	const groups = top.filter((e) => e.isIndex && !HIDDEN_LAST.has(e.key)).map((e) => toItem(e, 0));
	const loosePages = top.filter((e) => !e.isIndex).map((e) => ({ slug: e.id }));
	const tail = top.filter((e) => HIDDEN_LAST.has(e.key)).map((e) => ({ ...toItem(e, 1), collapsed: true }));
	return [
		{ label: 'Home', slug: tree.prefix },
		...groups,
		{ label: 'Other pages', collapsed: true, items: [...loosePages, ...tail] },
	];
}

export function buildSidebar() {
	return TREES.map((t) => ({ label: t.key, items: treeSidebar(t) }));
}
