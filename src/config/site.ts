/**
 * 站点身份信息：改这一个文件，全站生效。
 * 标题、署名、导航、社交链接都在这里。
 */
export const siteConfig = {
  /** 浏览器标签页与页脚使用的完整站点名 */
  title: 'Roject 的博客',
  /** 页头 Logo 与大字排版使用的短名（建议全大写拉丁字母） */
  shortTitle: 'ROJECT',
  /** 站点副标题，出现在页头 Logo 下方 */
  subtitle: 'PERSONAL ARCHIVE',
  /** 作者署名 */
  author: 'Roject',
  /** 首页大标题下方的自我介绍 */
  tagline: '在噪声中，保持清醒的记录。',
  /** SEO 描述 */
  description:
    'Roject 的个人博客：学习与科研笔记、编程技术、摄影影像与社会观察。写作是反抗遗忘的方式，也是把混乱整理成线索的过程。',
  /** 站点语言 */
  lang: 'zh-CN',
  /** 建站年份，用于页脚版权 */
  since: 2026,
  /** GitHub 主页（页脚与关于页展示） */
  github: 'https://github.com/Roject-CN',
  /** RSS 路径 */
  rss: '/rss.xml',
  /** 顶部导航 */
  nav: [
    { index: '01', label: '文章', href: '/blog/' },
    { index: '02', label: '影像', href: '/photos/' },
    { index: '03', label: '归档', href: '/archive/' },
    { index: '04', label: '关于', href: '/about/' },
  ],
  /** SEO 关键词 */
  keywords: ['个人博客', '学习笔记', '编程', '摄影', '社会观察', 'Astro', 'GitHub Pages'],
};

export type SiteConfig = typeof siteConfig;