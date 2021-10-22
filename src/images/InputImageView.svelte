<script>
import ImageView from './ImageView.svelte';
import { imgPath, imgDir, imgIdx } from '../serverImgStores';
import { Tooltip } from 'svelma';

let promise;
let files = [];
$: if($imgDir != null) promise = getInputImagesInfo($imgDir);

async function getInputImagesInfo(dir) {
    const url = `/images/${dir}`;
    const res = await fetch(url);
    const resJson = await res.json();
    if(res.ok) {
        files = resJson.filter(f => f.type === 'file').map(f => f.name);
        return resJson;
    }
    else throw new Error(resJson);
}

function changeIdx(e, change) {
    const newIdx = (e != null) ? parseInt(e.target.value) : $imgIdx + change;
    const newImgPath = `/images/${$imgDir}/${files[newIdx]}`;
    if (newIdx >= 0 && newIdx <= files.length) {
        imgIdx.set(newIdx);
        imgPath.set(newImgPath);
    } else console.error(`Cannot change idx ${$imgIdx} to ${newIdx}; out of bounds error`);
}
</script>

<div class="p-3">
    <div class="header-space-between mb-3">
        <div class="is-size-5 pr-3">Input</div>
        <div>
            {#if promise}
                {#await promise}
                    <i class="fas fa-circle-notch fa-spin has-text-info"></i>
                {:then response}
                    <i class="fas fa-check-circle has-text-success"></i>
                {:catch error}
                    <Tooltip label={error}>
                        <i class="fas fa-times-circle has-text-danger"></i>
                    </Tooltip>
                {/await}
            {:else}
                <i class="fas fa-exclamation-triangle has-text-warning"></i>
            {/if}
        </div>
    </div>
    {#if $imgDir}
        <ImageView image={`${$imgPath}?processed`} advanced={true} />
        <div class="imageIdxChanger mt-3 mx-3">
            <div on:click={()=> {changeIdx(null, -1)}}><i class="mx-3 fas fa-chevron-left"></i></div>
            <input type="range" min={0} max={files.length} value={$imgIdx} on:change={changeIdx} />
            <div on:click={()=> {changeIdx(null, 1)}}><i class="mx-3 fas fa-chevron-right"></i></div>
        </div>
        <div class="folderWrapper mt-1 mx-3">
            <i class="m-1 fas fa-folder-open has-text-warning"></i> 
            <div class="m-1">{$imgDir}</div>
        </div>
        <div class="folderWrapper mt-1 mx-3">
            <i class="m-1 fas fa-image has-text-info"></i> 
            <div class="m-1">{$imgIdx} / {files.length}</div>
        </div>
    {/if}
</div>

<style lang="scss">
.folderWrapper {
    display: flex;
    align-items: center;
    justify-content: center;
}
.imageIdxChanger {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.imageIdxChanger .fas {
    transition: opacity 0.3ms ease-in-out;
    opacity: 0.7;
    &:hover {
        opacity: 1;
    }
}
</style>
