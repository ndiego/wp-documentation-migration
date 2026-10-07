// A bare VideoPress URL on its own line (WordPress auto-embeds it) -> responsive iframe,
// plus the visible link underneath as a fallback. Preview only; docs/ keeps the bare URL.
const VP = /^https:\/\/videopress\.com\/v\/([A-Za-z0-9]+)\/?$/;

export default function remarkVideopress() {
	return (tree) => {
		tree.children.forEach((node, i) => {
			if (node.type !== 'paragraph' || node.children.length !== 1) return;
			const c = node.children[0];
			const url = c.type === 'link' ? c.url : c.type === 'text' ? c.value.trim() : '';
			const m = VP.exec(url);
			if (!m) return;
			tree.children[i] = {
				type: 'html',
				value: `<figure class="videopress-embed"><iframe src="https://videopress.com/embed/${m[1]}?hd=1" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen title="VideoPress video"></iframe><figcaption><a href="${url}">${url}</a></figcaption></figure>`,
			};
		});
	};
}
