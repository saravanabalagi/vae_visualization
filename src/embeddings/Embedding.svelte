<script>
    import { modEmbedding, customImg, serverImgPath } from "../stores";
    import { Button, Tooltip } from 'svelma';
    
    let embedding = [];
    let values = [];
    let promise;

    // values are modified as slider moves
    // use on change to avoid multiple requests
    // $:{ modEmbedding.set(values); }

    $:if ($serverImgPath != null) promise = getEmbeddingForImgPath($serverImgPath);
    else promise = getEmbedding($customImg);

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

    async function getEmbeddingForImgPath(imgPath) {
        const url = imgPath.replace('/images', '/embedding');
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

<div class="embeddingView p-3">
    <div class="header-space-between mb-3">
        <div class="is-size-5">Embedding</div>
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
    <div class="embeddingSlidersWrapper">
        {#if embedding.length > 0}
            <div>
                {#each embedding as number, i}
                    <div class="sliderRow">
                        <input type=range min={-1.5} max={1.5} step={0.01} bind:value={values[i]} on:change={setModEmbedding} />
                        <div class="mx-3 numDisplay has-text-right">{values[i].toFixed(2)}</div>
                        <Tooltip label={number.toFixed(2)} position="is-right">
                            <div class="undo" 
                                class:show={(number.toFixed(2) !== values[i].toFixed(2))} 
                                on:click={() => resetEmbeddingAt(i)}>
                                <i class="fas fa-undo-alt"></i>
                            </div>
                        </Tooltip>
                    </div>
                {/each}
            </div>
            <Button class="my-3" type="is-danger" on:click={() => resetEmbeddingAt()}>Reset All</Button>
        {/if}
    </div>
</div>

<style>
    .embeddingView {
        padding: 10px;
        min-width: 200px;
    }
    .numDisplay {
        display: inline-block;
        width: 50px;
    }
    .sliderRow {    
        display: flex;
        align-items: center;
    }
    .embeddingSlidersWrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .undo { 
        transition: opacity 0.3s ease-in-out; 
        opacity: 0; 
    }
    .undo.show { opacity:0.7; }
    .sliderRow:hover .undo { opacity: 0.7; }
    .sliderRow:hover .undo:hover { opacity: 1; }
</style>
