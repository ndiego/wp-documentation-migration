import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
// @ts-ignore plain JS helper
import { idFromDocsPath } from '../lib/paths.mjs';

// Starlight's docsLoader() is hard-wired to src/content/docs. We use Astro's glob loader
// directly so the collection reads ../docs in place (no symlink, no copy), and we generate
// ids from the file path so README.md becomes the folder index route. Without generateId,
// the glob loader would use the frontmatter `slug` as id and flatten every URL.
export const collections = {
	docs: defineCollection({
		loader: glob({
			base: '../docs',
			pattern: ['**/*.md', '!assets/**'],
			generateId: ({ entry }) => idFromDocsPath(entry),
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
