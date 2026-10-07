// The WordPress importer needs `# Title` as the first body line, but Starlight already
// renders the frontmatter title. Drop the first top-level H1 so it isn't shown twice.
export default function remarkStripFirstH1() {
	return (tree) => {
		const i = tree.children.findIndex((n) => n.type === 'heading');
		if (i !== -1 && tree.children[i].depth === 1) tree.children.splice(i, 1);
	};
}
