import { writable } from 'svelte/store';

export const inputImageFile = writable();
export const inputImage = writable();
export const embedding = writable([]);
export const modEmbedding = writable([]);
export const outputImage = writable();
