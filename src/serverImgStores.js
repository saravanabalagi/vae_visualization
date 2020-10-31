import { derived, writable } from "svelte/store";
import path from 'path';

export const fileExt = writable('png');
export const numDigits = writable(5);
export const imgIdx = writable(null);
export const imgDir = writable(null);

export const imgPath = derived(
        [imgDir, imgIdx, numDigits, fileExt], 
        ([imgDir, imgIdx, numDigits, fileExt]) => {
            if ([imgDir, imgIdx, numDigits, fileExt].some(e => e == null)) return null;
            let imgIdxPadded = String(imgIdx).padStart(numDigits, '0');
            let imgFilename = imgIdxPadded + fileExt;
            return path.join(imgDir, imgFilename);
        }
    );


export const setImgPathVars = (imgPathArg) => {
    if (imgPathArg == null) {
        imgIdx = null;
        return;
    }
    let fileExtL = path.extname(imgPathArg);
    fileExt.set(fileExtL);
    numDigits.set(path.basename(imgPathArg, fileExtL).length);
    imgIdx.set(parseInt(path.basename(imgPathArg, fileExtL)));
    imgDir.set(path.basename(path.dirname(imgPathArg)));
}
