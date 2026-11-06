---
title: 写作手册：这个博客支持哪些 Markdown 写法
description: 一份给未来的自己看的排版说明：frontmatter、标题、图片、代码、表格、提示框与草稿。
date: 2026-09-18
tags: ['指南', '技术']
cover: /images/covers/markdown.jpg
coverAlt: 荧光绿与黑色警示条纹构成的抽象图像
---

这篇既是文章，也是这个博客的写作说明书。下次忘了某个格式怎么写，回来翻这一页就行。

## 新建一篇文章

推荐用脚手架：

```bash
npm run new -- "文章标题" my-post-slug
```

它会在 `src/content/blog/` 下生成一个带 frontmatter 的 Markdown 文件。也可以手动新建，文件名建议用 `YYYY-MM-DD-slug.md`。

## Frontmatter

每篇文章开头必须有一段 YAML：

```yaml
---
title: 文章标题
description: 一句话摘要，会出现在列表、搜索和 SEO 里
date: 2026-09-18
tags: ['指南', '技术']
cover: /images/covers/markdown.jpg
coverAlt: 封面的替代文字
featured: false
pinned: false
draft: false
---
```

字段说明：

| 字段 | 必填 | 作用 |
| --- | --- | --- |
| `title` | 是 | 标题，最长 80 字 |
| `description` | 是 | 摘要，最长 240 字 |
| `date` | 是 | 发布日期，决定排序 |
| `tags` | 否 | 标签数组，会自动生成标签页 |
| `cover` | 否 | 封面图路径，放在 `public/images/covers/` |
| `featured` | 否 | 是否参与首页精选 |
| `pinned` | 否 | 是否置顶 |
| `draft` | 否 | 草稿不会出现在任何页面和 RSS 中 |

## 标题与目录

正文用 `##` 和 `###` 两级标题即可，右侧目录会自动生成。

> 提示：文章里尽量只用一个 `#` 标题——就是 frontmatter 里的 `title`。正文从 `##` 开始。

## 图片与图注

普通图片：

```md
![替代文字](/images/posts/example.jpg)
```

需要图注时，用 HTML 的 `figure`：

```html
<figure>
  <img src="/images/posts/example.jpg" alt="替代文字" />
  <figcaption>这里是图注。</figcaption>
</figure>
```

## 代码块

用三个反引号包裹，并标注语言，构建时会自动高亮：

```js
const greet = (name) => `你好，${name}`;
console.log(greet('Roject'));
```

代码块右上角有复制按钮。

## 引用与提示

普通引用：

> 写作是反抗遗忘的方式，也是把混乱整理成线索的过程。

需要强调一段话时，可以用提示框：

<div class="callout">
  <strong>注意：</strong>这是一个自定义提示框。它没有依赖任何插件，只是 Markdown 里的一个 HTML 块。
</div>

## 列表与任务

- 无序列表
- 第二项
  - 嵌套一项

1. 有序列表
2. 第二项

- [x] 已完成的写作
- [ ] 还没写完的部分

## 表格

| 格式 | 写法 | 效果 |
| --- | --- | --- |
| 粗体 | `**文字**` | **文字** |
| 斜体 | `*文字*` | *文字* |
| 行内代码 | `` `code` `` | `code` |
| 链接 | `[文字](https://example.com)` | [文字](https://example.com) |

## 草稿与发布

写完但还没准备好公开时，在 frontmatter 里加：

```yaml
draft: true
```

构建时它会自动被排除。确认无误后改成 `false`，提交即可。

## 发布

```bash
git add .
git commit -m "post: 写作手册"
git push
```

推送到 `main` 分支后，GitHub Actions 会自动构建并部署。通常一两分钟后就能在线上看到。

---

如果格式上还有不确定的地方，直接看这篇文章的源文件：`src/content/blog/2026-09-18-markdown-guide.md`。它本身就是最好的样例。