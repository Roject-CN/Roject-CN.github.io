---
title: 用 Astro + GitHub Pages 搭一个可长期维护的博客
description: 从内容集合、图片优化到自动部署：这套博客的技术栈、目录结构与取舍。
date: 2026-10-20
tags: ['技术', '教程']
cover: /images/covers/astro.jpg
coverAlt: 紫色网格与六边形构成的抽象图像
---

这个博客没有后台，也不需要服务器。它的全部工作流程可以压缩成一句话：**写 Markdown，提交到 Git，GitHub Actions 自动构建并发布。**

下面是我在搭它时做的几个关键选择，以及为什么。

## 为什么是 Astro

静态站点生成器很多，我选 Astro 主要因为三点：

1. **默认零 JavaScript**。页面以 HTML 为主，交互脚本按需加载，首屏很轻。
2. **内容集合自带类型校验**。文章的 frontmatter 如果写错字段，构建会直接报错，而不是悄悄生成一个空页面。
3. **图片处理是内置的**。`astro:assets` 会自动生成多尺寸、现代格式的图片，不需要额外插件。

它也支持 React、Vue 等框架，但这个博客完全没用——用原生 HTML 和一点 vanilla JS 就够了。

## 目录结构

```text
Blog/
├─ src/
│  ├─ content/blog/        # 文章：一个 Markdown 一个文件
│  ├─ assets/photos/       # 相册原图（构建时优化）
│  ├─ pages/               # 路由：首页、文章、标签、影像、搜索
│  ├─ components/          # 页头、页脚、卡片等
│  └─ styles/global.css    # 全站设计系统
├─ public/images/          # 封面、文章插图、OG 图
├─ scripts/new-post.mjs    # 新建文章的脚手架
└─ .github/workflows/      # 自动部署
```

文章的 URL 直接来自文件名：`2026-11-06-hello-world.md` 会变成 `/blog/2026-11-06-hello-world/`。日期前缀让文件在文件夹里自然排序，也让 URL 自带时间信息。

## 一张图看懂构建流程

<figure>
  <img src="/images/posts/pipeline.svg" alt="从 Markdown 到 GitHub Pages 的构建流程图" width="820" height="780" />
  <figcaption>一次提交，触发一次完整的构建与发布。</figcaption>
</figure>

整个过程没有任何"服务器"参与。GitHub Actions 启动一个临时的 Ubuntu 环境，安装依赖、执行 `npm run build`，把生成的 `dist/` 目录作为静态站点发布。

## 部署工作流

核心配置只有几行：

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
```

第一次部署前，还需要在仓库的 **Settings → Pages → Build and deployment** 里把 Source 设为 **GitHub Actions**。之后每次 push 都会自动更新。

## 几个刻意的取舍

**不用数据库。** 文章就是文件，评论以后可以接 Giscus（基于 GitHub Discussions），不需要自己维护服务。

**不用 CSS 框架。** 设计系统是手写的一组 CSS 变量，改颜色只要改几行。代价是要自己处理响应式，但换来的是完全可控的视觉。

**固定版本。** `package.json` 里的 Astro 锁在 5.x，因为本机的 Node 20 足够跑，构建环境也稳定。升级留到真正需要的时候再做。

## 图片怎么处理

文章里的插图放在 `public/images/posts/`，用普通 Markdown 图片语法引用；相册图片放在 `src/assets/photos/`，由 Astro 自动压缩并生成 `srcset`。前者简单直接，后者适合大图。

具体流程写在《从相机到网页：我的照片工作流》里。

## 最后

这套方案不一定是"最好"的，但它足够简单，简单到我可以把注意力放在写作上，而不是维护博客上。

对一个个人项目来说，这大概就是最重要的指标。