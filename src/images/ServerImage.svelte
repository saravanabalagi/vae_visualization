<script>
import { customImg } from '../stores';
import { getImgFilePath, 
         numDigits as numDigitsStore, 
         fileExt as fileExtStore, 
         imgDir as imgDirStore, 
         imgIdx as imgIdxStore} from '../serverImgStores';
import ImageView from "./ImageView.svelte";
import path from 'path';

export let imgDir;
export let setLoading;
let imgPath;
let min, max, numDigits, fileExt, imgIdx;

$: imgRangePromise = getIndexRange(imgDir);
async function getIndexRange(imgDir) {
    setLoading(imgDir, true);
    const url = `/images/${imgDir}?info`;
    const res = await fetch(url);
    const resJson = await res.json();
    setLoading(imgDir, false);
    min = parseInt(resJson.first.split('.')[0]);
    max = parseInt(resJson.last.split('.')[0]);
    fileExt = path.extname(resJson.first);
    numDigits = path.basename(resJson.first, fileExt).length;
}

$: if(max > 0) {
    imgIdx = Math.floor(Math.random() * (max+1 - min) + min);
    imgPath = `/images/${getImgFilePath([imgDir, imgIdx, numDigits, fileExt])}`;
}

function saveImgPathToStore() {
    customImg.set(null);
    numDigitsStore.set(numDigits);
    fileExtStore.set(fileExt);
    imgDirStore.set(imgDir);
    imgIdxStore.set(imgIdx);
}
</script>

<div class="serverImage" on:click={saveImgPathToStore}>
    {#if imgPath != null}
        <ImageView image={imgPath} />
    {/if}
</div>

<style>
.serverImage {
    cursor: pointer;
}
</style>
