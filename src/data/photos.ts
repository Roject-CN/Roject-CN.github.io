import type { ImageMetadata } from 'astro';

import p1 from '../assets/photos/signal-01.jpg';
import p2 from '../assets/photos/signal-02.jpg';
import p3 from '../assets/photos/signal-03.jpg';
import p4 from '../assets/photos/signal-04.jpg';
import p5 from '../assets/photos/signal-05.jpg';
import p6 from '../assets/photos/signal-06.jpg';

export interface Photo {
  src: ImageMetadata;
  title: string;
  alt: string;
  album: string;
  date: string;
  caption: string;
}

/**
 * 添加照片的步骤：
 * 1. 把图片放进 src/assets/photos/（建议长边 1600–2400px，JPEG / WebP）
 * 2. 在下方 import 并追加一条记录
 * 3. album 相同的照片会自动归入同一个相册筛选
 */
export const photos: Photo[] = [
  {
    src: p1,
    title: '同步率测试',
    alt: '紫黑色同心圆与荧光刻度构成的抽象图像',
    album: '结构',
    date: '2026.10',
    caption: '同心圆与刻度：把仪表盘当作风景。',
  },
  {
    src: p2,
    title: '夜间地平线',
    alt: '深色背景上荧光绿色的水平扫描线',
    album: '光影',
    date: '2026.10',
    caption: '一条被荧光切开的水平线。',
  },
  {
    src: p3,
    title: '橙色警报',
    alt: '紫色渐变背景上的橙色圆形与网格',
    album: '光影',
    date: '2026.09',
    caption: '在紫色噪声里，橙色是唯一的路标。',
  },
  {
    src: p4,
    title: '垂直城市',
    alt: '紫色垂直线条与方块构成的抽象建筑',
    album: '结构',
    date: '2026.09',
    caption: '重复的窗格，重复的夜晚。',
  },
  {
    src: p5,
    title: '十字准星',
    alt: '黑色背景上的荧光绿十字准星与网格',
    album: '噪声',
    date: '2026.08',
    caption: '当所有信号归零，准星仍然指向某处。',
  },
  {
    src: p6,
    title: '噪点练习',
    alt: '黑色背景上的绿色噪点与故障条纹',
    album: '噪声',
    date: '2026.08',
    caption: '当信号消失，剩下的噪点也是一种纹理。',
  },
];

export const albums = [...new Set(photos.map((photo) => photo.album))];