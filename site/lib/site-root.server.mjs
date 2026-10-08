// The site folder for code that Vite bundles: Astro's own project root (the folder holding
// astro.config.mjs). Swapped in for lib/site-root.mjs by the "#site-root" alias in astro.config.mjs.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { root } from 'astro:config/server';

export const SITE_DIR = path.resolve(fileURLToPath(root));
