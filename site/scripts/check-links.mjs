// Link/anchor check over the built site (dist/).
// For every <a href>, <img src>, <video src/poster>, <source src> inside the Markdown
// content area of each page: internal URLs must resolve to a file in dist/ and a
// #fragment must match an id (or a[name]) in the target page.
// Usage: node scripts/check-links.mjs [--all] [--json out.json]
//   --all  also check links in Starlight's chrome (sidebar, header, pagination)
import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'node-html-parser';

const DIST = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../dist');
const args = process.argv.slice(2);
const ALL = args.includes('--all');
const jsonOut = args.includes('--json') ? args[args.indexOf('--json') + 1] : null;

const pages = [];
(function walk(dir) {
	for (const d of fs.readdirSync(dir, { withFileTypes: true })) {
		const p = path.join(dir, d.name);
		if (d.isDirectory() && !d.isSymbolicLink() && !['_astro', 'pagefind', 'assets'].includes(d.name)) walk(p);
		else if (d.isFile() && d.name.endsWith('.html')) pages.push(p);
	}
})(DIST);

const idCache = new Map();
const ids = (file) => {
	if (!idCache.has(file)) {
		const root = parse(fs.readFileSync(file, 'utf8'));
		const set = new Set();
		for (const el of root.querySelectorAll('[id]')) set.add(el.getAttribute('id'));
		for (const el of root.querySelectorAll('a[name]')) set.add(el.getAttribute('name'));
		idCache.set(file, set);
	}
	return idCache.get(file);
};

const resolveFile = (urlPath) => {
	const p = path.join(DIST, decodeURIComponent(urlPath));
	for (const c of [p, path.join(p, 'index.html'), p + '.html']) {
		try {
			if (fs.statSync(c).isFile()) return c;
		} catch {}
	}
	return null;
};

const stats = { pages: pages.length, links: 0, internal: 0, ok: 0, missingFile: 0, missingAnchor: 0, external: 0 };
const problems = [];
for (const file of pages) {
	const pageUrl = '/' + path.relative(DIST, file).replace(/index\.html$/, '').replace(/\\/g, '/');
	const root = parse(fs.readFileSync(file, 'utf8'));
	const scope = ALL ? root : root.querySelector('.sl-markdown-content');
	if (!scope) continue;
	const refs = [];
	for (const el of scope.querySelectorAll('a[href]')) refs.push(['href', el.getAttribute('href')]);
	for (const el of scope.querySelectorAll('img[src], video[src], source[src], audio[src]')) refs.push(['src', el.getAttribute('src')]);
	for (const el of scope.querySelectorAll('video[poster]')) refs.push(['poster', el.getAttribute('poster')]);
	for (const [kind, raw] of refs) {
		stats.links++;
		if (/^(https?:)?\/\//i.test(raw) || /^(mailto|tel|javascript|data):/i.test(raw)) {
			stats.external++;
			continue;
		}
		stats.internal++;
		let u;
		try {
			u = new URL(raw, 'http://x' + pageUrl);
		} catch {
			stats.missingFile++;
			problems.push({ page: pageUrl, kind, url: raw, problem: 'bad-url' });
			continue;
		}
		const target = resolveFile(u.pathname);
		if (!target) {
			stats.missingFile++;
			problems.push({ page: pageUrl, kind, url: raw, problem: 'missing-file' });
			continue;
		}
		// WordPress ids can contain literal %xx sequences (utf8_uri_encode), so accept the
		// fragment as written or percent-decoded.
		const rawFrag = raw.includes('#') ? raw.slice(raw.indexOf('#') + 1) : '';
		let decoded = rawFrag;
		try {
			decoded = decodeURIComponent(rawFrag);
		} catch {}
		// '#top' always scrolls to the top of the document per the HTML spec.
		if (rawFrag && rawFrag.toLowerCase() !== 'top' && target.endsWith('.html') && !ids(target).has(rawFrag) && !ids(target).has(decoded)) {
			stats.missingAnchor++;
			problems.push({ page: pageUrl, kind, url: raw, problem: 'missing-anchor' });
			continue;
		}
		stats.ok++;
	}
}
console.log(JSON.stringify(stats, null, 2));
const byKind = {};
for (const p of problems) byKind[p.problem] = (byKind[p.problem] ?? 0) + 1;
console.log('problems by type:', byKind);
for (const p of problems.slice(0, 40)) console.log(`  ${p.problem}\t${p.page}\t${p.url}`);
if (problems.length > 40) console.log(`  ... ${problems.length - 40} more`);
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify({ stats, problems }, null, 2));
process.exitCode = problems.length ? 1 : 0;
