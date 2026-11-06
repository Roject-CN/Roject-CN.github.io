import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

/**
 * 站点地址与子路径
 * ------------------------------------------------------------------
 * 如果你部署在 https://<用户名>.github.io/  （用户主页仓库），保持默认即可。
 * 如果你部署在 https://<用户名>.github.io/<仓库名>/（项目仓库），
 * 请在 GitHub 仓库的 Settings → Secrets and variables → Actions → Variables
 * 里添加 SITE_URL 与 BASE_PATH，工作流会自动注入。
 */
const SITE_URL = process.env.SITE_URL || 'https://roject-cn.github.io';
const BASE_PATH = process.env.BASE_PATH || '/';
const BASE_PREFIX = BASE_PATH === '/' ? '' : BASE_PATH.replace(/\/+$/, '');

/**
 * 让 Markdown 里的绝对路径自动带上部署子路径。
 * 例如 BASE_PATH=/blog/ 时，![](/images/a.jpg) 会输出为 /blog/images/a.jpg。
 */
function remarkBasePath() {
  return (tree) => {
    if (!BASE_PREFIX) return;

    const visit = (node) => {
      if (typeof node.url === 'string' && node.url.startsWith('/') && !node.url.startsWith('//')) {
        node.url = `${BASE_PREFIX}${node.url}`;
      }
      if (node.type === 'html' && typeof node.value === 'string') {
        node.value = node.value.replace(/\b(src|href)="\/(?!\/)/g, `$1="${BASE_PREFIX}/`);
      }
      if (Array.isArray(node.children)) node.children.forEach(visit);
    };

    visit(tree);
  };
}

export default defineConfig({
  site: SITE_URL,
  base: BASE_PATH,
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404') && !page.includes('/search/'),
    }),
  ],
  markdown: {
    remarkPlugins: [remarkBasePath],
    shikiConfig: {
      theme: 'vitesse-dark',
      wrap: true,
    },
  },
});