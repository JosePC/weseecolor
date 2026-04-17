// @ts-check
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import react from '@astrojs/react';
import markdoc from '@astrojs/markdoc';
import keystatic from '@keystatic/astro';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://weseecolor.net',
  output: 'server',
  adapter: cloudflare({
    imageService: 'compile',
  }),
  integrations: [react(), markdoc(), keystatic(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
    server: {
      fs: {
        // Prevent dev server from serving files outside src/public/etc.
        // Blocks accidental leaks of legacy/ WP assets via URL traversal.
        allow: ['.'],
        deny: ['legacy/**'],
      },
    },
  },
});
