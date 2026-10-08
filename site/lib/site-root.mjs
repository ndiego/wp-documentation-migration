// The site folder (site/) for code that Node loads directly: astro.config.mjs and everything it
// imports (remark/rehype plugins, sidebar, integrations). Resolved via the "#site-root" import in
// package.json. Code that Vite bundles (pages, components, route middleware, content config) gets
// lib/site-root.server.mjs instead through a resolve.alias in astro.config.mjs, because a bundled
// copy of this file would resolve import.meta.url to a chunk under dist/.
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const SITE_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
