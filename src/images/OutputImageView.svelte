<script>
import { modEmbedding, outputImage } from '../stores';
import ImageView from './ImageView.svelte';
import { Tooltip } from 'svelma'; 

$:promise = getOutputImage($modEmbedding);
async function getOutputImage(modEmbedding) {
    const url = '/decoded_img';
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
                <Tooltip label={error}>
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
</div>
