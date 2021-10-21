<script>
import { customImg as customImgStore } from '../stores';
import { imgDir as imgDirStore,
         imgIdx as imgIdxStore, 
         imgPath as imgPathStore } from '../serverImgStores';
import ImageView from "./ImageView.svelte";

export let imgDir;
export let setLoading;
let imgPath;
let imgIdx;
let files = [];

$: getFilesPromise = getFiles(imgDir);
async function getFiles(imgDir) {
    setLoading(true);
    const url = `/images/${imgDir}`;
    const res = await fetch(url);
    const resJson = await res.json();
    files = resJson.filter(f => f.type === 'file').map(f => f.name);
    setLoading(false);
}

$: if(files.length > 0) {
    const min = 0;
    const max = files.length;
    imgIdx = Math.floor(Math.random() * (max+1 - min) + min);
    imgPath = `/images/${imgDir}/${files[imgIdx]}`;
}

function saveImgPathToStore() {
    customImgStore.set(null);
    imgPathStore.set(imgPath);
    imgIdxStore.set(imgIdx);
    imgDirStore.set(imgDir);
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
