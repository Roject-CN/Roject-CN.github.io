# Roject 的博客

一个用 **Astro 5 + GitHub Pages** 搭建的静态个人博客。没有数据库、没有后台、没有追踪脚本，文章和图片都以文件形式保存在 Git 仓库里。

设计上借了《新世纪福音战士》的一点配色：紫黑底色、荧光绿信号、橙色警告。但阅读体验优先——排版、目录、图片和搜索都为长文服务。

![首页预览](docs/preview-home.jpg)

---

## 已经实现的功能

**内容**
- Markdown 文章，frontmatter 带类型校验，字段写错会在构建时报错
- 草稿（`draft: true`）自动从页面、RSS 和搜索中排除
- 标签系统：标签索引页 + 单标签文章列表
- 按年份归档
- 置顶 / 首页精选
- 上一篇 / 下一篇 + 基于标签的相关文章
- 阅读时长估算、自动目录、滚动高亮
- 代码高亮 + 一键复制、表格、引用、自定义提示框
- RSS 订阅、sitemap、robots.txt、SEO meta、Open Graph、JSON-LD

**图片**
- 封面图、文章插图、独立相册三种图片位置
- 相册使用 `astro:assets` 自动生成多尺寸 WebP，手机不会下载原图
- 相册支持按专辑筛选、灯箱浏览、键盘左右切换
- 首页图片预览条

**体验**
- 深色 / 浅色主题，默认深色，可切换并记住选择
- 构建时生成全文搜索索引，纯前端搜索，无第三方服务
- 响应式布局（桌面 / 平板 / 手机）
- 无障碍：跳转链接、键盘焦点、`aria` 标签、`prefers-reduced-motion`
- 页面滚动显现等轻量动效

**工程**
- 一条命令新建文章
- GitHub Actions 自动构建并发布到 GitHub Pages
- 支持「用户主页仓库」和「项目仓库」两种路径（自动处理 `base`）
- 零客户端框架，默认不加载任何 JavaScript 框架运行时

---

## 本地运行

需要 **Node.js 20+**（推荐 20 LTS）和 npm。本机在 Node 20.16 上验证通过。

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # 构建到 dist/
npm run preview    # 本地预览构建结果
```

> 本项目固定使用 Astro `5.16.16`，因为它在 Node 20 上最稳定。升级 Astro 大版本前请先看官方迁移指南。

---

## 目录结构

```text
Blog/
├─ src/
│  ├─ config/site.ts          # 站点名称、署名、导航、社交链接
│  ├─ content/blog/           # 文章（Markdown）
│  ├─ content.config.ts       # 文章字段定义与校验
│  ├─ assets/photos/          # 相册原图（构建时优化）
│  ├─ data/photos.ts          # 相册元数据：标题、相册、图注
│  ├─ pages/                  # 路由
│  │  ├─ index.astro          # 首页
│  │  ├─ blog/                # 文章列表 + 详情
│  │  ├─ tags/                # 标签索引 + 标签页
│  │  ├─ photos/              # 影像库
│  │  ├─ archive.astro        # 归档
│  │  ├─ about.astro          # 关于
│  │  ├─ search.astro         # 搜索
│  │  ├─ rss.xml.ts           # RSS
│  │  └─ search.json.ts       # 搜索索引
│  ├─ components/             # 页头、页脚、卡片、核心图形等
│  ├─ layouts/                # BaseLayout / PostLayout
│  └─ styles/global.css       # 设计系统（颜色、字体、组件样式）
├─ public/
│  ├─ images/covers/          # 文章封面
│  ├─ images/posts/           # 文章插图
│  ├─ favicon.svg
│  └─ og-default.jpg          # 默认社交分享图
├─ scripts/
│  ├─ new-post.mjs            # 新建文章
│  └─ generate-demo-images.py # 重新生成演示图片（可选）
└─ .github/workflows/deploy.yml
```

---

## 写一篇文章

### 方式一：脚手架（推荐）

```bash
npm run new -- "文章标题" my-post-slug
```

会在 `src/content/blog/` 下生成 `2026-11-06-my-post-slug.md`，并带上 frontmatter。第二个参数可省略。

### 方式二：手动新建

文件名建议用 `YYYY-MM-DD-slug.md`，例如 `2026-11-06-hello-world.md`。URL 会变成 `/blog/2026-11-06-hello-world/`。

### Frontmatter 字段

```yaml
---
title: 文章标题                  # 必填，最长 80 字
description: 一句话摘要          # 必填，最长 240 字
date: 2026-11-06                # 必填，决定排序
updated: 2026-11-08             # 可选，显示“更新于”
tags: ['随笔', '技术']           # 可选，自动生成标签页
cover: /images/covers/hello.jpg # 可选，封面图
coverAlt: 封面的替代文字          # 可选，建议填写
featured: false                 # 可选，首页精选
pinned: false                   # 可选，首页置顶
draft: false                    # 可选，true 时不会发布
---
```

正文从 `##` 二级标题开始写。完整的 Markdown 示例见文章《写作手册：这个博客支持哪些 Markdown 写法》，源文件是 `src/content/blog/2026-09-18-markdown-guide.md`。

---

## 上传图片

### 1. 文章封面

放到 `public/images/covers/`，在 frontmatter 里写路径：

```yaml
cover: /images/covers/my-cover.jpg
```

建议尺寸 **1600 × 900**（16:9），JPEG 质量 80 左右。

### 2. 文章里的插图

放到 `public/images/posts/`，Markdown 里直接引用：

```md
![图片说明](/images/posts/2026-09-night-01.jpg)
```

需要图注时用：

```html
<figure>
  <img src="/images/posts/2026-09-night-01.jpg" alt="夜晚的江面" />
  <figcaption>风把水面吹皱，灯光碎成一片。</figcaption>
</figure>
```

### 3. 相册

相册图片放在 `src/assets/photos/`，然后在 `src/data/photos.ts` 里导入并追加一条记录：

```ts
import p7 from '../assets/photos/my-photo.jpg';

// 在 photos 数组里追加：
{
  src: p7,
  title: '江边的风',
  alt: '夜晚江面上的灯光倒影',
  album: '光影',          // 相同的 album 会自动归入同一个筛选
  date: '2026.11',
  caption: '风把水面吹皱，灯光碎成一片。',
}
```

构建时会自动生成 400 / 800 / 1200px 多种尺寸的 WebP，并输出 `srcset`。原图建议长边 **2000px** 左右、sRGB、JPEG 质量 80。

> 当前相册里的 6 张图是脚本生成的演示图，可以随时删除并替换成你自己的照片。

---

## 修改站点信息

大部分内容只需要改一个文件：`src/config/site.ts`。

```ts
export const siteConfig = {
  title: 'Roject 的博客',
  shortTitle: 'ROJECT',
  author: 'Roject',
  tagline: '在噪声中，保持清醒的记录。',
  description: '站点描述……',
  github: 'https://github.com/Roject-CN',
  nav: [ ... ],
};
```

想改颜色、字体、间距，编辑 `src/styles/global.css` 顶部的 CSS 变量：

```css
:root {
  --bg: #08080b;
  --violet: #8b5cf6;
  --acid: #c8ff3d;
  --orange: #ff5c2b;
}
```

---

## 部署到 GitHub Pages

### 第 1 步：创建仓库

推荐使用**用户主页仓库**，地址最干净：

- 仓库名：`<你的用户名>.github.io`
- 例如当前配置默认的 `https://roject-cn.github.io`，对应仓库 `roject-cn.github.io`
- 可见性必须是 **Public**（免费账户的 GitHub Pages 要求）

如果使用普通项目仓库（`https://<用户名>.github.io/<仓库名>/`），看第 4 步的变量配置。

### 第 2 步：推送代码

```bash
git init
git add .
git commit -m "init: personal blog"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

### 第 3 步：打开 Pages

仓库 **Settings → Pages → Build and deployment**：

- **Source** 选择 **GitHub Actions**
- 不需要选择分支，工作流会自己上传构建产物

推送后到 **Actions** 标签页看 `Deploy to GitHub Pages` 是否成功。首次部署通常需要 1–3 分钟。

### 第 4 步：项目仓库的路径配置

如果站点在子路径下（`https://user.github.io/repo/`），需要在仓库 **Settings → Secrets and variables → Actions → Variables** 添加：

| 变量 | 值 |
| --- | --- |
| `SITE_URL` | `https://<用户名>.github.io` |
| `BASE_PATH` | `/<仓库名>/` |

用户主页仓库则不需要设置，默认 `SITE_URL=https://roject-cn.github.io`、`BASE_PATH=/`。

### 自定义域名

1. 在 `public/` 下新建 `CNAME` 文件，内容写你的域名，例如 `blog.example.com`
2. 在域名服务商处添加一条 `CNAME` 记录指向 `<用户名>.github.io`
3. 在仓库 Settings → Pages → Custom domain 填写域名并开启 HTTPS
4. 把 `SITE_URL` 改成 `https://blog.example.com`（同时把 `BASE_PATH` 设为 `/`）

---

## 这个博客还能加什么

按「投入产出比」排序，供以后慢慢折腾：

1. **评论**：接入 [Giscus](https://giscus.app/)，基于 GitHub Discussions，免费、无广告、静态站点友好。
2. **访问统计**：Umami（可自托管）或 Plausible，轻量且不收集个人数据。
3. **Newsletter**：Buttondown / Substack 的嵌入表单，把 RSS 读者变成邮件订阅者。
4. **友链页面**：一个 `/friends/` 页面，互相导流，是独立博客的传统艺能。
5. **项目页**：`/projects/` 展示代码与作品，比 About 更适合放链接。
6. **书影音清单**：`/reading/`，用 Markdown 表格维护，比豆瓣更自由。
7. **OG 图片自动生成**：为每篇文章生成带标题的分享图（`satori` + `resvg`）。
8. **内容管理后台**：Decap CMS / TinaCMS，用 GitHub 登录后在网页里写文章。
9. **PWA / 离线阅读**：加一个 service worker，把最近文章缓存下来。
10. **中英双语**：Astro 的 i18n 路由 + 两份内容目录。

不建议一开始就全部加上。先写十篇文章，再决定哪个功能真的需要。

---

## 常见问题

**构建失败：`npm ci` 找不到 lock 文件？**
先本地执行 `npm install`，把生成的 `package-lock.json` 一起提交。

**线上页面 404 / 样式丢失？**
检查 `BASE_PATH` 是否和仓库类型匹配。项目仓库必须是 `/<仓库名>/`，用户主页仓库是 `/`。

**图片在本地正常，线上 404？**
`public/` 里的图片用 `/images/...` 路径即可；组件里引用时统一走 `withBase()` 帮助函数，它会自动补上子路径。

**换了域名后 RSS / sitemap 里的链接不对？**
修改 `SITE_URL` 环境变量（或 `astro.config.mjs` 里的默认值），重新构建。

**想改文章 URL？**
改文件名即可。旧链接会失效，个人博客一般可以接受；如果需要保留，可以加一条重定向。

---

## 说明

- 示例文章（6 篇）和演示图片仅用于展示版式，发布前建议替换成你自己的内容。
- 演示图片由 `scripts/generate-demo-images.py` 生成，重新运行即可再生成一套。
- 字体使用开源的 Rajdhani 与 JetBrains Mono（通过 `@fontsource` 本地打包），中文使用系统字体，不依赖外部 CDN。