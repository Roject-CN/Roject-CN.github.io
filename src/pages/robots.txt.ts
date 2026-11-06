import type { APIRoute } from 'astro';
import { withBase } from '../lib/url';

export const GET: APIRoute = ({ site }) => {
  const origin = site ?? new URL('https://example.com');
  const sitemap = new URL(withBase('/sitemap-index.xml'), origin);

  return new Response(`User-agent: *\nAllow: /\n\nSitemap: ${sitemap.href}\n`, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
};