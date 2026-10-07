// JS port of scripts/convert.py sanitize_title(), itself a port of WordPress
// sanitize_title_with_dashes($title, '', 'save'). The live HelpHub TOC
// (wporg/table-of-contents) builds heading ids with it, and the in-content #anchor
// links and <a id> lines produced by the converter depend on it.

export const RESERVED_IDS = new Set(['main', 'masthead', 'menu-header', 'page', 'primary', 'secondary',
	'secondary-content', 'site-navigation', 'wordpress-org', 'wp-toolbar', 'wpadminbar', 'wporg-footer',
	'wporg-header']);

const escapeHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** @param {string} text heading text (plain, decoded). It is re-escaped first so the
 *  entity rules match what the Python version saw (BeautifulSoup decode_contents()). */
export function sanitizeTitle(text) {
	let t = escapeHtml(text);
	t = t.replace(/<[^>]*>/g, '');
	t = t.normalize('NFKD').replace(/\p{M}/gu, '');
	t = t.replace(/ß/g, 'ss').replace(/æ/g, 'ae').replace(/Æ/g, 'AE').replace(/ø/g, 'o').replace(/Ø/g, 'O');
	t = t.toLowerCase();
	t = t.replace(/( |&nbsp;|&#160;|–|—|&ndash;|&#8211;|&mdash;|&#8212;)/g, '-');
	t = t.replace(/\//g, '-');
	t = t.replace(/[¡¿«»‹›‘’“”‚‛„‟•©®°…™´˝́̀̂̃̈]/g, '');
	t = t.replace(/&#(8216|8217|8220|8221|8230|8482|169|174|176|171|187|161|191|8226);/g, '');
	t = t.replace(/×/g, 'x');
	t = t.replace(/&.+?;/g, '');
	t = t.replace(/\./g, '-');
	// Non-ASCII letters that survive remove_accents get percent-encoded (utf8_uri_encode), lowercased.
	t = Array.from(t).map((c) => (c.codePointAt(0) < 128 ? c : encodeURIComponent(c).toLowerCase())).join('');
	t = t.replace(/[^%a-z0-9 _-]/g, '');
	t = t.replace(/\s+/g, '-');
	t = t.replace(/-+/g, '-');
	return t.replace(/^-+|-+$/g, '');
}

/** wporg/table-of-contents de-duplication: reserved ids and repeats get -2, -3, ... */
export function uniqueId(base, used) {
	let cand = base;
	let n = 2;
	while (used.has(cand) || RESERVED_IDS.has(cand)) cand = `${base}-${n++}`;
	used.add(cand);
	return cand;
}
