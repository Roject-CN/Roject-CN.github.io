#!/usr/bin/env node
/**
 * 把 Sveltia CMS 的浏览器资源从 node_modules 复制到 public/admin。
 * 这些文件体积较大，不提交到 Git；npm run dev / build 前会自动执行。
 */
import { cp, mkdir, readdir, rm, stat } from 'node:fs/promises';
import { join } from 'node:path';

const pkgDir = join(process.cwd(), 'node_modules', '@sveltia', 'cms');
const destDir = join(process.cwd(), 'public', 'admin');

async function copyTree(src, dest) {
  const info = await stat(src);
  if (info.isDirectory()) {
    await mkdir(dest, { recursive: true });
    for (const entry of await readdir(src)) {
      if (entry.endsWith('.map')) continue;
      await copyTree(join(src, entry), join(dest, entry));
    }
    return;
  }
  await cp(src, dest, { force: true });
}

await mkdir(destDir, { recursive: true });
await rm(join(destDir, 'sveltia-cms.js'), { force: true });
await rm(join(destDir, 'chunks'), { recursive: true, force: true });
await rm(join(destDir, 'locales'), { recursive: true, force: true });

await cp(join(pkgDir, 'dist', 'sveltia-cms.js'), join(destDir, 'sveltia-cms.js'));
await copyTree(join(pkgDir, 'dist', 'chunks'), join(destDir, 'chunks'));
await copyTree(join(pkgDir, 'locales'), join(destDir, 'locales'));

console.log('Sveltia CMS assets synced to public/admin');