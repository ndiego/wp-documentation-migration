// Project configuration for the @wporg-docs/screenshots engine (wp-screenshots). Paths are relative to this file.
export default {
	shotsDir: 'shots',
	outDir: '../docs/assets/screenshots',
	docsDir: '../docs',
	docsManifest: '../docs/manifest.json',
	blueprint: 'blueprint/blueprint.json',
	suitesDir: 'blueprint/suites',
	workDir: '.wp-screenshots',

	// Pinned environment. The blueprint's `preferredVersions` is authoritative; keep both in sync.
	wordpress: { version: '7.1.3', php: '8.3' },
	port: 9400,

	// Lossless WebP converts to PNG without loss if the decision ever changes.
	format: 'webp',

	// House style overrides (see packages/screenshots/src/style.js in the toolkit for every token).
	style: {},
};
