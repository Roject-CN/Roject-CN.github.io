/**
 * 同时兼容「用户主页仓库」与「项目仓库」两种 GitHub Pages 路径。
 * 例如 base 为 `/my-blog` 时，withBase('/blog/') -> '/my-blog/blog/'。
 */
const rawBase = import.meta.env.BASE_URL || '/';
const base = rawBase === '/' ? '' : rawBase.replace(/\/+$/, '');

export function withBase(path = '/'): string {
  if (/^(https?:)?\/\//i.test(path) || path.startsWith('mailto:') || path.startsWith('#')) {
    return path;
  }
  const clean = path.startsWith('/') ? path : `/${path}`;
  return `${base}${clean}`;
}

export function absoluteUrl(path: string, site?: URL): string {
  if (/^https?:\/\//i.test(path)) return path;
  const origin = site ?? new URL('http://localhost:4321');
  return new URL(withBase(path), origin).href;
}

/** 去掉子路径后的当前路径，用于导航高亮 */
export function currentPath(pathname: string): string {
  if (base && pathname.startsWith(base)) {
    const rest = pathname.slice(base.length);
    return rest.startsWith('/') ? rest : `/${rest}`;
  }
  return pathname || '/';
}