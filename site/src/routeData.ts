// Starlight route middleware: makes the single Starlight site behave like two sites.
//  - sidebar: keep only the group of the page's tree (see lib/sidebar.mjs), none elsewhere
//  - pagination: recomputed from that filtered sidebar so prev/next never crosses trees
//  - edit link: proposed -> GitHub edit on the restructure branch; current -> read-only
//    blob at the before-restructure tag (the old layout as committed there)
//  - <title>: suffixed with the tree name so browser tabs/history tell them apart
import path from 'node:path';
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
// @ts-ignore plain JS helper
import { SITE_DIR, treeForId } from '../lib/paths.mjs';

type Entry = { type: 'link'; isCurrent: boolean; href: string } | { type: 'group'; label: string; entries: Entry[] };

const flatten = (entries: Entry[]): Entry[] => entries.flatMap((e) => (e.type === 'group' ? flatten(e.entries) : [e]));

export const onRequest = defineRouteMiddleware((context) => {
	const route = context.locals.starlightRoute;
	const tree = treeForId(context.url.pathname);
	if (!tree) {
		route.sidebar = [];
		route.hasSidebar = false;
		return;
	}
	const group = (route.sidebar as Entry[]).find((e) => e.type === 'group' && e.label === tree.key) as Extract<Entry, { type: 'group' }> | undefined;
	route.sidebar = (group?.entries ?? []) as typeof route.sidebar;

	const links = flatten(route.sidebar as Entry[]);
	const i = links.findIndex((l) => l.type === 'link' && l.isCurrent);
	route.pagination = {
		prev: i > 0 ? (links[i - 1] as any) : undefined,
		next: i > -1 && i + 1 < links.length ? (links[i + 1] as any) : undefined,
	};

	const filePath = route.entry.filePath;
	if (filePath) {
		const rel = path.relative(tree.dir, path.resolve(SITE_DIR, filePath)).split(path.sep).join('/');
		route.editUrl = new URL(tree.sourceUrl(rel));
	}

	const title = route.head.find((h) => h.tag === 'title');
	if (title && typeof title.content === 'string') title.content = title.content.includes(' | ') ? title.content.replace(' | ', ` (${tree.short}) | `) : `${title.content} (${tree.short})`;
});
