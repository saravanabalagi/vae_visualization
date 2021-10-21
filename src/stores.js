import { writable } from 'svelte/store';

export const customImg = writable();
export const imgPath = writable();
export const imgDir = writable();
export const imgIdx = writable();

export const embedding = writable([]);
export const modEmbedding = writable([]);

export const outputImage = writable();
