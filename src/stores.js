import { writable } from 'svelte/store';

export const routes = writable();

export const customImg = writable();
export const imgPath = writable();
export const imgDir = writable();
export const imgIdx = writable();

export const embedding = writable([]);
export const modEmbedding = writable([]);

export const inputImage = writable();
export const outputImage = writable();
