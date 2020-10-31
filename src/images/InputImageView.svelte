<script>
import ImageView from './ImageView.svelte';
import { imgDir, imgIdx, fileExt, imgPath } from '../serverImgStores';
import { Tooltip } from 'svelma';
import path from 'path';

let promise;
let numFiles, firstFileIdx, lastFileIdx;
$: if($imgDir != null) promise = getInputImagesInfo($imgDir);

async function getInputImagesInfo(dir) {
    const url = `/images/${dir}?info`;
    let response = await fetch(url);
    let responseJson = await response.json();

    if(response.ok) {
        numFiles = responseJson.num_files;
        firstFileIdx = parseInt(path.basename(responseJson.first, $fileExt));
        lastFileIdx = parseInt(path.basename(responseJson.last, $fileExt));
        return responseJson;
    }
    else throw new Error(responseJson);
}

function changeIdx(e, change) {
    let newIdx = (e != null) ? e.target.value : $imgIdx + change;
    if (newIdx >= firstFileIdx && newIdx <= lastFileIdx) {
        imgIdx.set(newIdx);
    } else console.error(`Cannot change idx ${$imgIdx} to ${newIdx}; out of bounds error`);
}
</script>

<div class="p-3">
    <div class="header-space-between mb-3">
        <div class="is-size-5">Input</div>
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
    <ImageView image={($imgPath != null) ? path.join('/images', $imgPath || '') : null} />
    {#if $imgDir}
        <div class="imageIdxChanger mt-3 mx-3">
            <div on:click={()=> {changeIdx(null, -1)}}><i class="mx-3 fas fa-chevron-left"></i></div>
            <input type="range" min={firstFileIdx} max={lastFileIdx} value={$imgIdx} on:change={changeIdx} />
            <div on:click={()=> {changeIdx(null, 1)}}><i class="mx-3 fas fa-chevron-right"></i></div>
        </div>
        <div class="folderWrapper mt-1 mx-3">
            <i class="m-1 fas fa-folder-open has-text-warning"></i> 
            <div class="m-1">{$imgDir}</div>
        </div>
        <div class="folderWrapper mt-1 mx-3">
            <i class="m-1 fas fa-image has-text-info"></i> 
            <div class="m-1">{$imgIdx} / {numFiles}</div>
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
