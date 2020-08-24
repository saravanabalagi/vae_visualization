<script>
    import { modEmbedding } from "./stores";
	let inputImageFile;

	import {inputImage as inputImageStore, inputImageFile as inputImageFileStore} from './stores';
    const unsubscribeInputImageFile =  inputImageFileStore.subscribe(val => inputImageFile = val);
    
    let embedding = [];
    let values = [];
    let promise = getEmbedding(inputImageFile);

    async function getEmbedding(inputImageFile) {
        const url = '/upload_image';
        const data = new FormData();
        data.append('image', inputImageFile)
        const content = {
            method: 'POST',
            body: data
        };
        let response = await fetch(url, content);
        let responseJson = await response.json();
        embedding = responseJson.embedding || [];
        values = Array.from(embedding);

        if(response.ok) return responseJson;
        else throw new Error(responseJson);
    }

    function setModEmbedding() {
        modEmbedding.set(values);
    }

</script>

<div class="embeddingView">
    <h2>Embedding</h2>
    {#await promise}
        Loading...
    {:then response}
        {#each embedding as number, i}
            <div>
                <span>{number}</span>
                <input type=range min={-1} max={1} step={0.1} bind:value={values[i]} on:change={setModEmbedding} />
                <span class="numDisplay">{values[i]}</span>
            </div>
        {/each}
    {:catch error}
        Error loading embedding: {error}
    {/await}
</div>

<style>
    .embeddingView {
        padding: 10px;
    }
    .numDisplay {
        display: inline-block;
        width: 50px;
    }
</style>
