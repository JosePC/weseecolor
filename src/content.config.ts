// Content collections are managed by Keystatic (see keystatic.config.ts).
// This file disables Astro's auto-generated content collections for
// directories under src/content/ so they don't shadow Keystatic's reader.
import { defineCollection } from 'astro:content';

const empty = defineCollection({ loader: () => [] });

export const collections = {
  articles: empty,
  experts: empty,
  videos: empty,
  resources: empty,
  hubs: empty,
  pages: empty,
  settings: empty,
};
