import { derived, writable } from "svelte/store";
import path from 'path';

export const getImgFilePath = ([imgDir, imgIdx, numDigits, fileExt]) => {
    if ([imgDir, imgIdx, numDigits, fileExt].some(e => e == null)) return null;
    let imgIdxPadded = String(imgIdx).padStart(numDigits, '0');
    let imgFilename = imgIdxPadded + fileExt;
    return path.join(imgDir, imgFilename);
}

export const fileExt = writable('png');
export const numDigits = writable(5);
export const imgIdx = writable(null);
export const imgDir = writable(null);
export const imgPath = derived([imgDir, imgIdx, numDigits, fileExt], getImgFilePath);
