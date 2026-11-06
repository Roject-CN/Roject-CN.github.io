import { getCollection, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'blog'>;

export async function getPublishedPosts(): Promise<Post[]> {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export function formatDate(date: Date): string {
  const y = date.getUTCFullYear();
  const m = String(date.getUTCMonth() + 1).padStart(2, '0');
  const d = String(date.getUTCDate()).padStart(2, '0');
  return `${y}.${m}.${d}`;
}

export function isoDate(date: Date): string {
  return date.toISOString();
}

/** 中文按 400 字/分钟、英文按 220 词/分钟估算 */
export function readingTime(body = ''): number {
  const cn = (body.match(/[\u3400-\u9fff]/g) ?? []).length;
  const latin = body
    .replace(/[\u3400-\u9fff]/g, ' ')
    .split(/\s+/)
    .filter((word) => /[A-Za-z0-9]/.test(word)).length;
  return Math.max(1, Math.ceil(cn / 400 + latin / 220));
}

export function plainText(markdown = ''): string {
  return markdown
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/[#>*_`~|=-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function collectTags(posts: Post[]): Array<{ name: string; count: number }> {
  const counts = new Map<string, number>();
  for (const post of posts) {
    for (const tag of post.data.tags) {
      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }
  return [...counts.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, 'zh-CN'));
}

export function relatedPosts(current: Post, all: Post[], limit = 2): Post[] {
  return all
    .filter((post) => post.id !== current.id)
    .map((post) => ({
      post,
      score: post.data.tags.filter((tag) => current.data.tags.includes(tag)).length,
    }))
    .sort((a, b) => b.score - a.score || b.post.data.date.valueOf() - a.post.data.date.valueOf())
    .slice(0, limit)
    .map((item) => item.post);
}