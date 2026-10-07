// Heading ids following WordPress sanitize_title + -2/-3 dedupe (wporg/table-of-contents),
// instead of github-slugger. Starlight/Astro only assign ids to headings without one, so
// setting them here (before their rehypeHeadingIds) also makes the TOC use these ids.
import { toString } from 'hast-util-to-string';
import { visit } from 'unist-util-visit';
import { sanitizeTitle, uniqueId } from '../lib/sanitize-title.mjs';

export default function rehypeWpHeadingIds() {
	return (tree) => {
		const used = new Set();
		visit(tree, 'element', (node) => {
			if (!/^h[1-6]$/.test(node.tagName) || node.properties?.id) return;
			const text = toString(node);
			if (!text.trim()) return;
			const base = sanitizeTitle(text);
			if (!base) return;
			node.properties.id = uniqueId(base, used);
		});
	};
}
