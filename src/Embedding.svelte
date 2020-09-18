<script>
    import { modEmbedding, inputImageFile, selectedServerImgIndex } from "./stores";
    
    let embedding = [];
    let values = [];
    let promise;

    // values are modified as slider moves
    // use on change to avoid multiple requests
    // $:{ modEmbedding.set(values); }

    $:if ($selectedServerImgIndex != null) promise = getEmbeddingFromIdx($selectedServerImgIndex);
    else promise = getEmbedding($inputImageFile);

    async function getEmbedding(inputImageFile) {
        const url = '/embedding';
        const data = new FormData();
        data.append('image', inputImageFile)
        const content = {
            method: 'POST',
            body: data
        };
        let response = await fetch(url, content);
        let responseJson = await response.json();

        if(response.ok) {
            embedding = responseJson.embedding || [];
            values = Array.from(embedding);
            modEmbedding.set(values);
            return responseJson;
        }
        else throw new Error(responseJson);
    }

    async function getEmbeddingFromIdx(idx) {
        const url = `/embedding/${idx}`;
        let response = await fetch(url);
        let responseJson = await response.json();

        if(response.ok) {
            embedding = responseJson.embedding || [];
            values = Array.from(embedding);
            modEmbedding.set(values);
            return responseJson;
        }
        else throw new Error(responseJson);
    }

    function setModEmbedding() {
        modEmbedding.set(values);
    }

    function resetEmbeddingAt(i) {
        if(i!=null) values[i] = embedding[i];
        else values = [...embedding];
        modEmbedding.set(values);
    }

</script>

<div class="embeddingView">
    <h2>Embedding</h2>
    <div>
        {#await promise}
            Loading...
        {:then response}
            Loaded!
        {:catch error}
            Error loading embedding: {error}
        {/await}
    </div>
    <div>
        {#if embedding.length > 0}
            <div on:click={() => resetEmbeddingAt()}>Reset All</div>
            {#each embedding as number, i}
                <div>
                    <span class="numDisplay left" on:click={() => resetEmbeddingAt(i)}>{(number.toFixed(2) == values[i].toFixed(2)) ? "" : number.toFixed(2)}</span>
                    <input type=range min={-1.5} max={1.5} step={0.01} bind:value={values[i]} on:change={setModEmbedding} />
                    <span class="numDisplay right">{values[i].toFixed(2)}</span>
                </div>
            {/each}
        {/if}
    </div>
</div>

<style>
    .embeddingView {
        padding: 10px;
    }
    .numDisplay {
        display: inline-block;
        width: 50px;
    }
    .numDisplay.left { text-align: right; }
    .numDisplay.right { text-align: left; }
</style>
