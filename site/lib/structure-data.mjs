// Build-time access to the restructure data (data/restructure-map.json,
// data/structure-metrics.json, data/structure-review.md) and the "same page in the
// other tree" lookup used by the tree banner.
//
// Read with fs (not a Vite JSON import) so the files outside site/ need no Vite fs.allow
// changes in dev; everything here runs at build time only.
import fs from 'node:fs';
import path from 'node:path';
import { DATA_DIR, TREE, TREES, treeId, treeForId } from './paths.mjs';
import { loadTree } from './sidebar.mjs';

const readJson = (f) => JSON.parse(fs.readFileSync(path.join(DATA_DIR, f), 'utf8'));

let cache;
export function structureData() {
	if (cache) return cache;
	const map = readJson('restructure-map.json');
	const metrics = readJson('structure-metrics.json');
	const review = fs.readFileSync(path.join(DATA_DIR, 'structure-review.md'), 'utf8');
	for (const a of map) {
		a.current_id = treeId(TREE.current, a.before_path);
		a.proposed_id = treeId(TREE.proposed, a.after_path);
	}
	cache = { map, metrics, review, counterpart: buildCounterparts(map) };
	return cache;
}

const dirOf = (p) => p.split('/').slice(0, -1).join('/');
/** deepest folder (at most maxDepth levels) that holds more than half of the given article folders ('' = root) */
const majorityFolder = (dirs, maxDepth = Infinity) => {
	const counts = new Map();
	for (const d of dirs) {
		const parts = d.split('/').filter(Boolean);
		for (let i = 1; i <= Math.min(parts.length, maxDepth); i++) {
			const k = parts.slice(0, i).join('/');
			counts.set(k, (counts.get(k) ?? 0) + 1);
		}
	}
	let best = '';
	for (const [k, n] of counts) {
		if (n * 2 > dirs.length && k.split('/').length > (best ? best.split('/').length : 0)) best = k;
	}
	return best;
};

/**
 * id -> id of the equivalent page in the other tree.
 *  - articles: by slug via restructure-map (paths are what the map records; the slug in the
 *    frontmatter is the same key). A proposed section whose index is an article maps to that
 *    article's old location.
 *  - section pages: the deepest section in the other tree that holds most (> 50%) of this
 *    section's articles (so "Design blocks" -> ".../blocks/design"); top-level sections only
 *    look at top-level sections ("Customization" -> "Editing & design").
 *  - anything else (root pages like site-health): the same path if it exists, else the tree root.
 */
function buildCounterparts(map) {
	const out = new Map();
	for (const a of map) {
		out.set(a.current_id, a.proposed_id);
		out.set(a.proposed_id, a.current_id);
	}
	const sides = { current: ['before_path', 'after_path', TREE.proposed], proposed: ['after_path', 'before_path', TREE.current] };
	const known = new Map(TREES.map((t) => [t.key, new Set(loadTree(t).entries.map((e) => e.id))]));
	for (const t of TREES) {
		const [from, to, other] = sides[t.key];
		for (const e of loadTree(t).entries) {
			if (out.has(e.id)) continue;
			let target;
			if (e.isIndex) {
				const folder = dirOf(e.markdown_source);
				const inside = map.filter((a) => folder === '' || a[from].startsWith(folder + '/'));
				// Top-level sections map to a top-level section (Customization -> Editing & design),
				// not to whatever deep folder happens to hold most of their articles.
				const common = majorityFolder(inside.map((a) => dirOf(a[to])), folder.includes('/') ? Infinity : 1);
				target = common ? `${other.prefix}/${common.toLowerCase()}` : other.prefix;
			} else {
				const same = `${other.prefix}/${e.id.slice(t.prefix.length + 1)}`;
				target = known.get(other.key).has(same) ? same : other.prefix;
			}
			out.set(e.id, target);
		}
	}
	return out;
}

let titles;
/** id -> { tree, id, title, kind } of the equivalent page in the other tree.
 *  kind: 'article' (same article), 'section' (closest section), 'home' (tree root fallback). */
export function counterpartOf(id) {
	const tree = treeForId(id);
	if (!tree) return undefined;
	const other = tree.key === 'current' ? TREE.proposed : TREE.current;
	const { counterpart, map } = structureData();
	titles ??= new Map(TREES.flatMap((t) => loadTree(t).entries.map((e) => [e.id, e.title])));
	const target = counterpart.get(id) ?? other.prefix;
	const isArticle = map.some((a) => a.current_id === id || a.proposed_id === id);
	const samePath = target.slice(other.prefix.length) === id.slice(tree.prefix.length);
	return {
		tree: other,
		id: target,
		title: titles.get(target) ?? other.label,
		slug: map.find((a) => a.current_id === id || a.proposed_id === id)?.slug,
		kind: isArticle ? 'article' : samePath ? 'page' : target === other.prefix ? 'home' : 'section',
	};
}
