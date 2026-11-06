import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string().max(80),
    description: z.string().max(240),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    /** 封面图放在 public/images/covers/ 下，这里写 /images/covers/xxx.jpg */
    cover: z.string().optional(),
    coverAlt: z.string().optional(),
    /** 首页精选 */
    featured: z.boolean().default(false),
    /** 首页置顶 */
    pinned: z.boolean().default(false),
    /** 草稿不会出现在任何页面与 RSS 中 */
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };