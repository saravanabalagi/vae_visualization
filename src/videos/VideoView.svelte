<script>
import { routes } from '../stores';
import { imgDir } from '../serverImgStores';
import EmbeddingsDiff from '../embeddings/EmbeddingsDiff.svelte';
import { Tooltip } from 'svelma';

let embeddings = [];
let promise = getEmbeddings($imgDir);

async function getEmbeddings(dir) {
    const url = `${$routes.embeddings}/${dir}`;
    let response = await fetch(url);
    let responseJson = await response.json();

    if(response.ok) {
        embeddings = responseJson.embeddings || [];
        return responseJson;
    }
    else throw new Error(responseJson);
}
</script>

<div class="EmbeddingsView p-3">
    <div class="header-space-between mb-3">
        <div class="is-size-5">Embeddings</div>
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
    {#if embeddings.length > 0}
        <EmbeddingsDiff embeddingsOrig={embeddings} />
    {/if}
</div>

<style>
.EmbeddingsView {
    min-width: 200px;
}
</style>
