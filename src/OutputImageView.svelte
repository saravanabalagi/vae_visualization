<script>
    import {modEmbedding as modEmbeddingStore} from './stores';
	import ImageView from './ImageView.svelte';
    
    let modEmbedding;
    let outputImage;
    const unsubscribeModEmbedding =  modEmbeddingStore.subscribe(val => modEmbedding = val);

    $:promise = getOutputImage(modEmbedding);
    async function getOutputImage(modEmbedding) {
        const url = '/upload_embedding';
		const content = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({embedding: modEmbedding})
        };
        
        let response = await fetch(url, content);
        // display blob image https://stackoverflow.com/a/43871843/3125070
		const urlCreator = window.URL || window.webkitURL;
        outputImage = urlCreator.createObjectURL(await response.blob());

        if(response.ok) return outputImage;
        else throw new Error(await response.json());
    }
</script>

<div>
    <h2>Output</h2>
    {#await promise}
        Loading...
    {:then response}
        {#if outputImage}
            <ImageView image={outputImage} />
        {/if}
    {/await}
</div>
