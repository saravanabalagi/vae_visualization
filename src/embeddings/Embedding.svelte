<script>
import { modEmbedding, customImg } from '../stores';
import { imgPath } from '../serverImgStores';
import { Button, Tooltip } from 'svelma';
import path from 'path';
import EmbeddingCanvas from './EmbeddingCanvas.svelte';

let embeddingPrev = [];
let embedding = [];
let values = [];
let promise;

$:if ($imgPath != null) promise = getEmbeddingForImgPath($imgPath);
else if($customImg != null) promise = getEmbedding($customImg);

$: embeddingDiff = values.map((v, i) => v-embeddingPrev[i]);
const getMean = (array) => array.reduce((a, b) => a + b, 0) / array.length;
$: valuesMean = getMean(values);
$: embeddingDiffMean = getMean(embeddingDiff);

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
        embeddingPrev = [...embedding];
        embedding = responseJson.embedding || [];
        if (embeddingPrev.length == 0)
            embeddingPrev = [...embedding];
        values = Array.from(embedding);
        modEmbedding.set(values);
        return responseJson;
    }
    else throw new Error(responseJson);
}

async function getEmbeddingForImgPath(imgPath) {
    const url = path.join('/embedding', imgPath.slice(7));
    let response = await fetch(url);
    let responseJson = await response.json();

    if(response.ok) {
        embeddingPrev = [...embedding];
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

function setMean(e) {
    const m = parseFloat(e.target.value);
    values = values.map(e => m);
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
        <div class="is-size-5 pr-3">Embedding {values.length > 0 ? `(${values.length} dimensions)`: ''}</div>
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
    {#if embedding.length > 0}
        <div class="sliderRow master">
            <Tooltip label="Mean" position="is-bottom">
                <div class="sliderIdx mr-1">M</div>
            </Tooltip>
            <input type=range min={-1.5} max={1.5} step={0.01} value={valuesMean} on:change={setMean} />
            <div class="mx-2 numDisplay has-text-right">{valuesMean.toFixed(2)}</div>
            <Tooltip label={valuesMean.toFixed(2)} position="is-right">
                <div class="undo show mr-2"
                    on:click={() => resetEmbeddingAt()}>
                    <i class="fas fa-undo-alt"></i>
                </div>
            </Tooltip>
            {#if embeddingPrev.length > 0}
            <div class="mx-2">
                <div class="numDisplay has-text-right" 
                    class:green={embeddingDiffMean>0}
                    class:red={embeddingDiffMean<0}
                    >
                    {embeddingDiffMean.toFixed(2)}
                </div>
                <div class="has-text-right">
                    ({embeddingDiff.reduce((acc,v) => acc+Math.abs(v), 0).toFixed(2)})
                </div>
            </div>
            {/if}
        </div>
        <div class="canvasWrapper">
            <div style="margin-left: 55px">
                <EmbeddingCanvas embedding={values} maxValue={1.5} width={140} />
            </div>
            {#if embeddingPrev.length > 0}
                <div>
                    <EmbeddingCanvas embedding={values.map((v, i) => v-embeddingPrev[i])} maxValue={1.5} width={140} />
                </div>
            {/if}
        </div>
        <div class="embeddingSlidersWrapper">
            {#each embedding as number, i}
                <div class="sliderRow">
                    <div class="sliderIdx mr-1">{i}</div>
                    <input type=range min={-1.5} max={1.5} step={0.01} bind:value={values[i]} on:change={setModEmbedding} />
                    <div class="mx-2 numDisplay has-text-right">{values[i].toFixed(2)}</div>
                    <Tooltip label={number.toFixed(2)} position="is-left">
                        <div class="undo" 
                            class:show={(number.toFixed(2) !== values[i].toFixed(2))} 
                            on:click={() => resetEmbeddingAt(i)}>
                            <i class="fas fa-undo-alt"></i>
                        </div>
                    </Tooltip>
                    {#if embeddingPrev.length > 0}
                        <div class="mx-2 numDisplay has-text-right" 
                            class:green={embeddingDiff[i]>0}
                            class:red={embeddingDiff[i]<0}
                        >
                            {embeddingDiff[i].toFixed(2)}
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
.embeddingView {
    display: flex;
    flex-direction: column;
    padding: 10px;
    min-width: 420px;
}
.numDisplay {
    display: inline-block;
    width: 50px;
}
.sliderRow {    
    display: flex;
    align-items: center;
    padding: 0 20px;
}
.sliderRow .sliderIdx {
    text-align: right;
    color: #999;
    width: 30px;
}

.embeddingSlidersWrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow-y: auto;
    flex: 1 1 1px;
}
.undo { 
    transition: opacity 0.3s ease-in-out; 
    opacity: 0; 
}
.undo.show { opacity:0.7; }
.sliderRow:hover .undo { opacity: 0.7; }
.sliderRow:hover .undo:hover { opacity: 1; }

.sliderRow.master {
    align-self: flex-start;
    padding: 10px 20px;
    background: rgba(0,0,0,0.1);
    border-radius: 20px;
    min-height: 70px;
}
.canvasWrapper {
    padding: 15px 0;
    display: flex;
    justify-content: space-between;
}
.green { color: green; }
.red { color: red; }
</style>
