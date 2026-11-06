import type { APIRoute } from 'astro';
import { formatDate, getPublishedPosts, plainText } from '../lib/posts';
import { withBase } from '../lib/url';

export const GET: APIRoute = async () => {
  const posts = await getPublishedPosts();

  const payload = posts.map((post) => ({
    title: post.data.title,
    description: post.data.description,
    tags: post.data.tags,
    date: formatDate(post.data.date),
    url: withBase(`/blog/${post.id}/`),
    text: plainText(post.body ?? '').slice(0, 6000),
  }));

  return new Response(JSON.stringify(payload), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
    },
  });
};