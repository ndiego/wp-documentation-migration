import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
// @ts-ignore plain JS helper
import { idFromRepoPath } from '../lib/trees.mjs';

// Starlight's docsLoader() is hard-wired to src/content/docs. We use Astro's glob loader
// directly so the collection reads the trees in place (no symlink, no copy), and we generate
// ids from the file path so README.md becomes the folder index route. Without generateId,
// the glob loader would use the frontmatter `slug` as id and flatten every URL.
//
// Two trees, one collection: Starlight renders exactly one `docs` collection, so a single
// glob loader with base = repo root reads both trees and prefixes the ids:
//   docs/**          -> proposed/...   (new tree)
//   build/before/**  -> current/...    (old category tree, scripts/build_all.sh)
// (Two glob loaders cannot share one collection: each one deletes the entries it did not see.)
export const collections = {
	docs: defineCollection({
		loader: glob({
			base: '..',
			pattern: ['docs/**/*.md', 'build/before/**/*.md', '!docs/assets/**', '!build/before/assets/**'],
			generateId: ({ entry }) => idFromRepoPath(entry),
		}),
		schema: docsSchema({
			// The docs/ frontmatter is importer/migration metadata, not Starlight's. Allow it.
			extend: z.looseObject({
				slug: z.string().optional(),
				original_url: z.string().url().optional(),
				wp_id: z.number().optional(),
				wp_category_id: z.number().optional(),
				categories: z.array(z.string()).optional(),
				date: z.string().optional(),
				modified: z.string().optional(),
				migration: z.record(z.string(), z.unknown()).optional(),
			}),
		}),
	}),
};
