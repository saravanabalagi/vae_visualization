<script>
import { modEmbedding, customImg } from '../stores';
import { imgPath } from '../serverImgStores';
import { Tooltip, Tag } from 'svelma';
import { getMean, getStd, getRandn, getLNorm } from '../utils';
import path from 'path';
import EmbeddingCanvas from './EmbeddingCanvas.svelte';
import EmbeddingStats from './EmbeddingStats.svelte';
import EmbeddingStatsConcise from './EmbeddingStatsConcise.svelte';

let embeddingPrev = [];
let embedding = [];
let values = [];

$:if ($imgPath != null) promise = getEmbeddingForImgPath($imgPath);
else if($customImg != null) promise = getEmbedding($customImg);

$: valuesMean = getMean(values);
$: valuesStd = getStd(values);
$: valuesL1 = getLNorm(values, 1);

$: valuesMeanDiff = getMean(values) - getMean(embeddingPrev);
$: valuesStdDiff = getStd(values) - getStd(embeddingPrev);
$: valuesL1Diff = getLNorm(values, 1) - getLNorm(embeddingPrev, 1);

$: embeddingDelta = values.map((v, i) => v-embeddingPrev[i]);
$: embeddingDeltaMean = getMean(embeddingDelta);
$: embeddingDeltaStd = getStd(embeddingDelta);
$: embeddingDeltaL1 = getLNorm(embeddingDelta, 1);

const ops = {
    'sum': () => values = values.map(v => v + operand),
    'sub': () => values = values.map(v => v - operand),
    'mul': () => values = values.map(v => v * operand),
    'div': () => values = values.map(v => v / operand),
    'const': () => values = values.map(v => operand),
}
let operand = 0.1;

const opsSample = {
    'normal': sampleRandn,
    'uniform': sampleRandu,
    'invert': additiveInvert,
}

let showFullTable = false;

let promise;

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
        if (embeddingPrev.length === 0)
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

function additiveInvert() {
    values = values.map(v => -v);
    modEmbedding.set(values);
}

function setModEmbedding() {
    modEmbedding.set(values);
}

function sampleRandn() {
    values = embedding.map(v => getRandn());
    modEmbedding.set(values);
}

function sampleRandu() {
    values = embedding.map(v => Math.random() - 0.5);
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
                <Tooltip label={error} position="is-bottom">
                    <i class="fas fa-times-circle has-text-danger"></i>
                </Tooltip>
            {/await}
        </div>
    </div>
    {#if embedding.length > 0}
        {#if showFullTable}
            <EmbeddingStats embedding={values} embeddingPrev={embeddingPrev} />
        {:else}
            <div class="px-5 pt-2 pb-1">
                <EmbeddingStatsConcise name="stats" mu={valuesMean} sigma={valuesStd} l1={valuesL1} />
            </div>
            {#if embeddingPrev.length > 0}
                <div class="px-5 pt-1 pb-2">
                    <EmbeddingStatsConcise mu={valuesMeanDiff} sigma={valuesStdDiff} l1={valuesL1Diff} diff={true} />
                </div>
            {/if}
        {/if}
        <div class="embeddingOperation m-2">
            <input class="operand" type="number" step={0.01} bind:value={operand} />
            {#each Object.keys(ops) as op}
                <div on:click={() => { ops[op](); setModEmbedding(); }} class='operation mx-1'><Tag>{op}</Tag></div>
            {/each}
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
        <div class="embeddingOperation m-2">
            {#each Object.keys(opsSample) as op}
                <div on:click={opsSample[op]} class='operation mx-1'><Tag>{op}</Tag></div>
            {/each}
            <div on:click={() => resetEmbeddingAt(null)} class='operation mx-1'><Tag type="is-danger">reset</Tag></div>
            <div on:click={() => showFullTable = !showFullTable} class='operation mx-1'><Tag type={showFullTable? "is-info" : "is-none"}>full stats</Tag></div>
        </div>
        {#if embeddingPrev.length > 0 && !showFullTable}
            <div class="px-5 py-3">
                <EmbeddingStatsConcise name="δ stats" mu={embeddingDeltaMean} sigma={embeddingDeltaStd} l1={embeddingDeltaL1} />
            </div>
        {/if}
        <div class="embeddingSlidersWrapper">
            {#each embedding as number, i}
                <div class="sliderRow">
                    <div class="sliderIdx mr-1">{i}</div>
                    <input type=range min={-1.5} max={1.5} step={0.01} bind:value={values[i]} on:change={setModEmbedding} />
                    <div class="mx-2 numDisplay has-text-right">{values[i].toFixed(2)}</div>
                    <div class="is-flex-grow-1">
                        <Tooltip label={number.toFixed(2)} position="is-left">
                            <div class="undo" 
                                class:show={(number.toFixed(2) !== values[i].toFixed(2))} 
                                on:click={() => resetEmbeddingAt(i)}>
                                <i class="fas fa-undo-alt"></i>
                            </div>
                        </Tooltip>
                    </div>
                    {#if embeddingPrev.length > 0}
                        <div class="mx-2 numDisplay has-text-right" 
                            class:green={embeddingDelta[i]>0}
                            class:red={embeddingDelta[i]<0}
                        >
                            {embeddingDelta[i].toFixed(2)}
                        </div>
                    {/if}
                </div>
            {/each}
        </div>
    {/if}
</div>

<style lang="scss">
.master {
    padding: 10px 0px;
    background: rgba(0,0,0,0.1);
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    > div {
        display: flex;
        align-items: center;
    }
}
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
.stats {
    padding: 10px 40px;
    justify-content: space-between;
}
.sliderRow {    
    display: flex;
    align-items: center;
    padding: 0 20px;
    width: 100%;
    .sliderIdx {
        text-align: right;
        color: #999;
        width: 30px;
    }
    &:hover .undo { opacity: 0.7; }
    &:hover .undo:hover { opacity: 1; }
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
    &.show { opacity:0.7; }
}

.canvasWrapper {
    padding: 15px 0;
    display: flex;
    justify-content: space-between;
}
.embeddingOperation {
    display: flex;
    justify-content: center;
    align-items: center;
    .operation {
        cursor: pointer;
        user-select: none;
    }
    .operand {
        width: 60px;
    }
}
.green { color: green; }
.red { color: red; }
</style>
