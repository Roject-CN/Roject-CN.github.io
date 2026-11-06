#!/usr/bin/env node
/**
 * 新建一篇文章：
 *   npm run new -- "文章标题" my-post-slug
 * 第二个参数可省略，省略时文件名为 YYYY-MM-DD-post.md。
 */
import { existsSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const args = process.argv.slice(2);
const title = (args[0] ?? '').trim();

if (!title) {
  console.error('用法：npm run new -- "文章标题" [英文-slug]');
  process.exit(1);
}

const now = new Date();
const ymd = [
  now.getFullYear(),
  String(now.getMonth() + 1).padStart(2, '0'),
  String(now.getDate()).padStart(2, '0'),
].join('-');

const rawSlug = (args[1] ?? 'post').trim().toLowerCase();
const slug =
  rawSlug
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60) || 'post';

let filename = `${ymd}-${slug}.md`;
const dir = join(process.cwd(), 'src', 'content', 'blog');
let fullPath = join(dir, filename);
let counter = 2;
while (existsSync(fullPath)) {
  filename = `${ymd}-${slug}-${counter}.md`;
  fullPath = join(dir, filename);
  counter += 1;
}

const body = `---
title: ${JSON.stringify(title)}
description: 在这里写一句话摘要，会出现在列表、搜索和 SEO 里。
date: ${ymd}
tags: []
draft: true
---

在这里开始写正文。

## 第一个小标题

写点什么。
`;

writeFileSync(fullPath, body, 'utf8');

console.log(`\n已创建：src/content/blog/${filename}`);
console.log('提示：');
console.log('  1. 修改 frontmatter 里的 description / tags');
console.log('  2. 写完把 draft 改成 false');
console.log('  3. npm run dev 预览，git push 后自动发布\n');