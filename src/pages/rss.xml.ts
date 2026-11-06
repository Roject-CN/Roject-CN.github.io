import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { getPublishedPosts } from '../lib/posts';
import { withBase } from '../lib/url';
import { siteConfig } from '../config/site';

export async function GET(context: APIContext) {
  const posts = await getPublishedPosts();

  return rss({
    title: siteConfig.title,
    description: siteConfig.description,
    site: context.site ?? 'https://example.com',
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description,
      link: withBase(`/blog/${post.id}/`),
      categories: post.data.tags,
    })),
    customData: `<language>${siteConfig.lang}</language>`,
  });
}