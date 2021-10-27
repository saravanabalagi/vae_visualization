<script>
import { routes, modEmbedding, outputImage, inputImage } from '../stores';
import ImageView from './ImageView.svelte';
import { Tooltip } from 'svelma'; 

$:promise = getOutputImage($modEmbedding);
async function getOutputImage(modEmbedding) {
    const url = $routes.decoded_img;
    const content = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({embedding: modEmbedding})
    };
    
    if(modEmbedding.length === 0) return;
    let response = await fetch(url, content);
    // display blob image https://stackoverflow.com/a/43871843/3125070
    const urlCreator = window.URL || window.webkitURL;
    const responseImage = urlCreator.createObjectURL(await response.blob());

    if(response.ok) {
        outputImage.set(responseImage);
        await getImgDiff();
        return responseImage;
    }
    else throw new Error(await response.json());
}

let imgDiff;
async function getImgDiff() {
    const url = $routes.img_compare_gray;
    const data = new FormData();
    const getBlob = async (url) => await fetch(url).then(r => r.blob());
    if ($inputImage == null || $outputImage == null) {
        setTimeout(getImgDiff, 1000);
        return; 
    }
    data.append('image_1', await getBlob($inputImage));
    data.append('image_2', await getBlob($outputImage));
    const content = {
        method: 'POST',
        body: data
    };
    const response = await fetch(url, content);
    const urlCreator = window.URL || window.webkitURL;
    const responseImage = urlCreator.createObjectURL(await response.blob());
    if (response.ok) {
        imgDiff = responseImage;
        return responseImage;
    }
    else throw new Error(await response.json());
}
</script>

<div class="p-3">
    <div class="header-space-between mb-3">
        <div class="is-size-5 pr-3">Reconstruction</div>
        <div>
            {#await promise}
                <i class="fas fa-circle-notch fa-spin has-text-info"></i>
            {:then response}
                <i class="fas fa-check-circle has-text-success"></i>
            {:catch error}
                <Tooltip label={error} position="is-bottom">
                    <i class="fas fa-times-circle has-text-danger"></i>
                </Tooltip>
            {/await}
        </div>
    </div>
    <div>
        {#if $outputImage}
            <ImageView image={$outputImage} advanced={true} />
        {/if}
    </div>
    <div class="mt-5 flex-column is-align-items-center">
        {#if imgDiff}
            <div class="p-2">
                Pixel Diff
            </div>
            <ImageView image={imgDiff} advanced={true} />
        {/if}
    </div>
</div>
