<script>
    import ImageView from './ImageView.svelte';
    import { inputImage } from 'stores';
    import { Tooltip } from 'svelma';

    let imgsDir, promise, imgIdx;
    let numFiles, firstFileIdx, lastFileIdx, fileExt, numDigits;
    $: if($inputImage) {
        let inputFilePathTokens = $inputImage.split('/');
        imgIdx = parseInt(inputFilePathTokens[inputFilePathTokens.length-1].split('.')[0]);
        imgsDir = inputFilePathTokens.slice(2, -1).join('/');
        promise = getInputImagesInfo(imgsDir);
    }
 
    async function getInputImagesInfo(dir) {
        const url = `/images/${dir}?info`;
        let response = await fetch(url);
        let responseJson = await response.json();

        if(response.ok) {
            numFiles = parseInt(responseJson.num_files);
            let filename = responseJson.first;
            let filenameTokens = filename.split('.');
            numDigits = filenameTokens[0].length;
            fileExt = filenameTokens[1];
            firstFileIdx = parseInt(filenameTokens[0]);
            lastFileIdx = parseInt(responseJson.last.split('.')[0]);
            return responseJson;
        }
        else throw new Error(responseJson);
    }

    function changeIdx() {
        let inputFilePathTokens = $inputImage.split('/');
        let imgIdxPadded = String(imgIdx).padStart(numDigits, '0');
        let imgFilename = `${imgIdxPadded}.${fileExt}`;
        inputFilePathTokens[inputFilePathTokens.length-1] = imgFilename;
        let newImgPath = inputFilePathTokens.join('/');
        getIdxForImgPath(newImgPath);
    }
    
    async function getIdxForImgPath(imgPath) {
        const url = imgPath.replace('/images', '/image_idx');
        let response = await fetch(url);
        let responseJson = await response.json();

        if(response.ok) {
            let idx = responseJson.idx;
            inputImage.set(imgPath);
            return responseJson;
        }
        else throw new Error(responseJson);
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
    <ImageView image={$inputImage} />
    {#if imgsDir}
        <div class="imageIdxChanger mt-3 mx-3">
            <div on:click={()=> {imgIdx = (imgIdx-1>=firstFileIdx) ? imgIdx-1 : imgIdx; changeIdx()}}><i class="mx-3 fas fa-chevron-left"></i></div>
            <input type="range" min={firstFileIdx} max={lastFileIdx} bind:value={imgIdx} on:change={changeIdx} />
            <div on:click={()=> {imgIdx = (imgIdx+1<=lastFileIdx) ? imgIdx+1 : imgIdx; changeIdx()}}><i class="mx-3 fas fa-chevron-right"></i></div>
        </div>
        <div class="folderWrapper mt-1 mx-3">
            <i class="m-1 fas fa-folder-open has-text-warning"></i> 
            <div class="m-1">{imgsDir}</div>
        </div>
        <div class="folderWrapper mt-1 mx-3">
            <i class="m-1 fas fa-image has-text-info"></i> 
            <div class="m-1">{imgIdx} / {numFiles}</div>
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
