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
	];
}

/** Collapsible tree (nested <details>) for one tree, as an HTML string. */
export function treeHtml(tree) {
	const { map } = structureData();
	const { childrenOf } = loadTree(tree);
	const pathKey = tree.key === 'current' ? 'before_path' : 'after_path';
	const count = (folder) => map.filter((a) => a[pathKey].startsWith(folder + '/')).length;
	const node = (e, depth) => {
		const href = esc(routeFromId(e.id));
		if (!e.isIndex) return `<li><a href="${href}">${esc(e.title)}</a></li>`;
		const n = count(e.key);
		const kids = childrenOf(e.key).map((c) => node(c, depth + 1)).join('');
		return `<li><details${depth === 0 ? ' open' : ''}><summary><a href="${href}">${esc(e.title)}</a> <span class="cmp-count" title="${n} article${n === 1 ? '' : 's'}">${n}</span></summary><ul>${kids}</ul></details></li>`;
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
	const misfiled = map.filter((a) => successor[top(a.after_path)] !== top(a.before_path)).sort(byTitle);
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
	return { misfiled, indexes, navRemoved, navBySection, uncategorized, topMoves };
}

export { TREE, TREES, esc, routeFromId };
