// Data preparation for the compare page (src/pages/compare/index.astro). Build time only.
import { TREE, TREES, routeFromId } from './paths.mjs';
import { loadTree } from './sidebar.mjs';
import { structureData } from './structure-data.mjs';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const fmt = (n, digits = 0) => (typeof n === 'number' ? n.toLocaleString('en-US', { maximumFractionDigits: digits }) : n);
const pct = (x) => `${Math.round(x * 100)}%`;

/** Headline metrics rows: [label, before, after, definition key] */
export function metricRows() {
	const { metrics } = structureData();
	const { before: b, after: a } = metrics;
	const none = '—';
	return [
		{ label: 'Articles', before: fmt(b.articles), after: fmt(a.articles) },
		{ label: 'Sections (folders)', before: fmt(b.folders), after: fmt(a.folders), def: 'folders' },
		{ label: 'Maximum depth', before: fmt(b.max_depth), after: fmt(a.max_depth), def: 'depth' },
		{ label: 'Mean depth', before: fmt(b.mean_depth, 2), after: fmt(a.mean_depth, 2), def: 'depth' },
		{
			label: 'Articles per section (median)',
			before: `${fmt(b.articles_per_folder.median, 1)} (max ${fmt(b.articles_per_folder.max)})`,
			after: `${fmt(a.articles_per_folder.median, 1)} (max ${fmt(a.articles_per_folder.max)})`,
			def: 'articles_per_folder',
		},
		{ label: 'Sections with a hand-written overview page', before: fmt(b.folders_with_index_page), after: fmt(a.folders_with_index_page), def: 'folders_with_index_page', note: b.folders_with_index_page_note },
		{ label: 'Sections using an article as their overview', before: fmt(b.sections_using_article_as_index), after: fmt(a.sections_using_article_as_index) },
		{
			label: 'Article order within a section',
			before: `${b.ordering.label} (${pct(b.ordering.non_alphabetical_share)} of ${b.ordering.folders_considered} sections not A–Z)`,
			after: `${a.ordering.label} (${pct(a.ordering.non_alphabetical_share)} of ${a.ordering.folders_considered} sections not A–Z)`,
			def: 'ordering',
		},
		{ label: 'Manual "Go back to…" breadcrumb paragraphs', before: fmt(b.manual_breadcrumb_paragraphs), after: fmt(a.manual_breadcrumb_paragraphs), def: 'manual_breadcrumb_paragraphs' },
		{ label: 'Articles that changed folder', before: none, after: `${fmt(a.articles_moved)} of ${fmt(a.articles)}`, def: 'articles_moved' },
		{ label: 'Articles whose folder title changed', before: none, after: `${fmt(a.articles_moved_by_folder_title)} of ${fmt(a.articles)}`, def: 'articles_moved_by_folder_title' },
		{ label: 'Misfiled articles moved to the right top-level section', before: none, after: fmt(a.misfiled_fixed), def: 'misfiled_fixed' },
		{ label: 'Orphan articles (no inbound link)', before: fmt(b.orphan_articles), after: fmt(a.orphan_articles), def: 'orphan_articles' },
		{ label: 'Classic-era articles', before: fmt(b.classic_articles), after: fmt(a.classic_articles), def: 'classic_articles' },
		{
			label: 'Classic articles outside a Classic WordPress section',
			before: fmt(b.classic_articles_outside_classic_section),
			after: fmt(a.classic_articles_outside_classic_section),
			def: 'classic_articles_outside_classic_section',
		},
		{
			label: 'Sections mixing classic and block-first articles',
			before: fmt(b.sections_mixing_classic_and_current),
			after: fmt(a.sections_mixing_classic_and_current),
			def: 'sections_mixing_classic_and_current',
		},
	];
}

const CLASSIC_BADGE = '<span class="cmp-classic" title="Classic WordPress: applies to classic themes or the Classic Editor plugin">classic</span>';

/** Collapsible tree (nested <details>) for one tree, as an HTML string. Classic-era articles get a
 *  "classic" badge in both trees (from the map's is_classic); proposed classic sections are badged too, and
 *  current sections show how many classic-era articles they hold, so reviewers see where they were scattered. */
export function treeHtml(tree) {
	const { map } = structureData();
	const { childrenOf } = loadTree(tree);
	const pathKey = tree.key === 'current' ? 'before_path' : 'after_path';
	const idKey = tree.key === 'current' ? 'current_id' : 'proposed_id';
	const classicIds = new Set(map.filter((a) => a.is_classic).map((a) => a[idKey]));
	const inFolder = (folder) => map.filter((a) => a[pathKey].startsWith(folder + '/'));
	const node = (e, depth) => {
		const href = esc(routeFromId(e.id));
		if (!e.isIndex) return `<li${classicIds.has(e.id) ? ' class="is-classic"' : ''}><a href="${href}">${esc(e.title)}</a>${classicIds.has(e.id) ? ' ' + CLASSIC_BADGE : ''}</li>`;
		const inside = inFolder(e.key);
		const n = inside.length;
		const nClassic = inside.filter((a) => a.is_classic).length;
		// proposed: the section itself is classic (manifest flag); current: a hint of how many classic pages it mixes in
		let badge = '';
		if (tree.key === 'proposed' && e.classic) badge = ' ' + CLASSIC_BADGE;
		else if (tree.key === 'current' && nClassic)
			badge = ` <span class="cmp-classic cmp-classic--count" title="${nClassic} classic-era article${nClassic === 1 ? '' : 's'} in this section">${nClassic} classic</span>`;
		const kids = childrenOf(e.key).map((c) => node(c, depth + 1)).join('');
		return `<li><details${depth === 0 ? ' open' : ''}><summary><a href="${href}">${esc(e.title)}</a> <span class="cmp-count" title="${n} article${n === 1 ? '' : 's'}">${n}</span>${badge}</summary><ul>${kids}</ul></details></li>`;
	};
	return `<ul class="cmp-tree">${childrenOf('').map((e) => node(e, 0)).join('')}</ul>`;
}

/** Compact rows for the "find your article" search (embedded as JSON in the page). */
export function searchRows() {
	return structureData().map.map((a) => ({
		t: a.title,
		s: a.slug,
		b: a.before_section,
		a: a.after_section,
		cu: routeFromId(a.current_id),
		pu: routeFromId(a.proposed_id),
	}));
}

/** "What changed" lists derived from the map. */
export function changes() {
	const { map, metrics } = structureData();
	const successor = metrics.after.top_level_successor;
	const top = (p) => p.split('/')[0];
	const byTitle = (x, y) => x.title.localeCompare(y.title);
	// classic articles moved for the block-first rule, not because they were misfiled (same rule as the metric)
	const misfiled = map.filter((a) => !a.is_classic && successor[top(a.after_path)] !== top(a.before_path)).sort(byTitle);
	// block-first: classic articles grouped by their proposed sub-section (Classic WordPress › X), in tree order
	const classicGroups = [];
	const { childrenOf } = loadTree(TREE.proposed);
	const treeOrder = new Map();
	const walk = (key) => childrenOf(key).forEach((e) => (treeOrder.set(e.id, treeOrder.size), walk(e.key)));
	walk('');
	const rank = (a) => treeOrder.get(a.proposed_id) ?? Infinity;
	for (const a of map.filter((x) => x.is_classic).sort((x, y) => rank(x) - rank(y))) {
		const group = a.after_section.slice(0, 2).join(' › ');
		let g = classicGroups.find((x) => x.title === group);
		if (!g) classicGroups.push((g = { title: group, folder: a.after_path.split('/').slice(0, 2).join('/'), articles: [] }));
		g.articles.push(a);
	}
	const indexes = map.filter((a) => a.after_is_section_index).sort(byTitle);
	const navRemoved = map.filter((a) => a.nav_link_removed);
	const navBySection = Object.entries(
		navRemoved.reduce((acc, a) => ((acc[a.before_section.join(' › ')] = (acc[a.before_section.join(' › ')] ?? 0) + 1), acc), {}),
	).sort((x, y) => y[1] - x[1]);
	const uncategorized = map.filter((a) => top(a.before_path) === 'uncategorized').sort(byTitle);
	const topMoves = Object.entries(
		map.reduce((acc, a) => {
			const k = `${a.before_section[0]} → ${a.after_section[0]}`;
			acc[k] = (acc[k] ?? 0) + 1;
			return acc;
		}, {}),
	).sort((x, y) => y[1] - x[1]);
	return { misfiled, indexes, navRemoved, navBySection, uncategorized, topMoves, classicGroups };
}

export { TREE, TREES, esc, routeFromId };
