// GitHub alerts (`> [!NOTE]`) -> Starlight asides.
// Starlight 0.42 has no native support for GitHub alert syntax (only `:::note` directives),
// so we rewrite the blockquote into the same mdast `containerDirective` node that
// remark-directive would produce for `:::note`. Starlight's own remark-asides plugin runs
// after user plugins and turns it into its <aside class="starlight-aside ..."> markup.
const MAP = { NOTE: 'note', TIP: 'tip', IMPORTANT: 'note', WARNING: 'caution', CAUTION: 'danger' };
const MARKER = /^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*(\r?\n)?/i;

export default function remarkGithubAlerts() {
	return (tree) => {
		const walk = (node) => {
			if (!node.children) return;
			node.children.forEach((child, i) => {
				if (child.type === 'blockquote') {
					const p = child.children[0];
					const first = p?.type === 'paragraph' ? p.children[0] : undefined;
					const m = first?.type === 'text' ? MARKER.exec(first.value) : null;
					if (m) {
						first.value = first.value.slice(m[0].length);
						if (first.value === '') p.children.shift();
						// A leading <br> right after the marker (seen in some converted content) is noise.
						while (p.children[0]?.type === 'break' || (p.children[0]?.type === 'html' && /^<br\s*\/?>$/i.test(p.children[0].value))) p.children.shift();
						if (p.children.length === 0) child.children.shift();
						node.children[i] = {
							type: 'containerDirective',
							name: MAP[m[1].toUpperCase()],
							attributes: {},
							children: child.children,
							position: child.position,
						};
					}
				}
				walk(node.children[i]);
			});
		};
		walk(tree);
	};
}
