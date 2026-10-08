// Where the two documentation trees live on disk, on top of the pure helpers in lib/trees.mjs.
// Both trees share ../docs/assets (build/before/assets is a symlink to it), served at /assets.
import path from 'node:path';
// lib/site-root.mjs (import.meta.url) when Node loads this via astro.config.mjs;
// lib/site-root.server.mjs (Astro's `root` from astro:config/server) in Vite-bundled code.
import { SITE_DIR } from '#site-root';
import { TREES as BASE_TREES, treeForId as baseTreeForId } from './trees.mjs';

export { idFromDocsPath, treeId, idFromRepoPath, routeFromId } from './trees.mjs';
export { SITE_DIR };
export const REPO_DIR = path.resolve(SITE_DIR, '..');
export const DOCS_DIR = path.join(REPO_DIR, 'docs');
export const BEFORE_DIR = path.join(REPO_DIR, 'build/before');
export const DATA_DIR = path.join(REPO_DIR, 'data');
export const ASSETS_DIR = path.join(DOCS_DIR, 'assets');

/** lib/trees.mjs TREES plus `dir`, the tree's absolute folder */
export const TREES = BASE_TREES.map((t) => ({ ...t, dir: path.join(REPO_DIR, t.src) }));
export const TREE = Object.fromEntries(TREES.map((t) => [t.key, t]));

/** absolute file path -> tree (or undefined) */
export function treeForFile(abs) {
	const p = path.resolve(abs);
	return TREES.find((t) => p.startsWith(t.dir + path.sep));
}

/** route id / pathname -> tree (or undefined) */
export function treeForId(id) {
	return TREE[baseTreeForId(id)?.key];
}
