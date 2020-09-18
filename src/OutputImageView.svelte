<script>
    import { modEmbedding, outputImage } from './stores';
	import ImageView from './ImageView.svelte';

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

<div>
    <h2>Output</h2>
    <div>
        {#await promise}
            Loading...
        {:then response}
            Loaded!
        {/await}
    </div>
    <div>
        {#if $outputImage}
            <ImageView image={$outputImage} />
        {/if}
    </div>
</div>
