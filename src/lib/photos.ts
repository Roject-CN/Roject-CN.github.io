import { getCollection, type CollectionEntry } from 'astro:content';

export type Photo = CollectionEntry<'photos'>;

export async function getPhotos(): Promise<Photo[]> {
  const photos = await getCollection('photos');
  return photos.sort(
    (a, b) => (a.data.order ?? 0) - (b.data.order ?? 0) || b.data.date.localeCompare(a.data.date),
  );
}

export function getAlbums(photos: Photo[]): string[] {
  return [...new Set(photos.map((photo) => photo.data.album))];
}

export function photoRawPath(photo: Photo): string {
  return photo.data.src.src;
}