<script>
import { customImg } from '../stores';
import { setImgPathVars } from '../serverImgStores';
import ImageView from "./ImageView.svelte";
import path from 'path';

export let idx;
export let setLoading;
let imgPath;

$: imagePathPromise = getImagePath(idx);
async function getImagePath(idx) {
    setLoading(idx, true);
    const url = `/image_paths/${idx}`
    const res = await fetch(url);
    const resJson = await res.json();
    setLoading(idx, false);
    imgPath = resJson.path;
    return resJson.path;
}

function saveImgPathToStore() {
    customImg.set(null);
    setImgPathVars(imgPath);
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
