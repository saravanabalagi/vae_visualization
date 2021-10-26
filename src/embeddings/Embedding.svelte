<script>
import { modEmbedding, customImg } from '../stores';
import { imgPath } from '../serverImgStores';
import { Tooltip, Tag } from 'svelma';
import { getMean, getStd, getRandn } from '../utils';
import path from 'path';
import EmbeddingCanvas from './EmbeddingCanvas.svelte';

let embeddingPrev = [];
let embedding = [];
let values = [];
const ops = {
    'sum': () => values = values.map(v => v + operand),
    'sub': () => values = values.map(v => v - operand),
    'mul': () => values = values.map(v => v * operand),
    'div': () => values = values.map(v => v / operand),
}
let operand = 0.1;
let promise;

$:if ($imgPath != null) promise = getEmbeddingForImgPath($imgPath);
else if($customImg != null) promise = getEmbedding($customImg);

$: embeddingDiff = values.map((v, i) => v-embeddingPrev[i]);

$: valuesMean = getMean(values);
$: valuesStd = getStd(values);
$: embeddingMeanDiff = getMean(embedding) - getMean(embeddingPrev);
$: embeddingDiffMean = getMean(embeddingDiff);
$: embeddingStdDiff = getStd(embedding) - getStd(embeddingPrev);
$: embeddingDiffStd = getStd(embeddingDiff);
$: embeddingDiffL1 = embeddingDiff.reduce((acc,v) => acc+Math.abs(v), 0);

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

function setModEmbedding() {
    modEmbedding.set(values);
}

function setMean(e) {
    const m = parseFloat(e.target.value);
    values = values.map(e => m);
    modEmbedding.set(values);
}

function setStd(e) {
    const sigma = parseFloat(e.target.value);
    values = embedding.map(v => getRandn());
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
        <div class="master">
            <div class="sliderRow mean">
                <Tooltip label="Mean" position="is-bottom">
                    <div class="sliderIdx mr-1">μ</div>
                </Tooltip>
                <input type=range min={-1.5} max={1.5} step={0.01} value={valuesMean} on:change={setMean} />
                <div class="mx-2 numDisplay has-text-right">{valuesMean.toFixed(2)}</div>
                <div class="is-flex-grow-1">
                    <Tooltip label={valuesMean.toFixed(2)} position="is-left">
                        <div class="undo show mr-2"
                            on:click={() => resetEmbeddingAt()}>
                            <i class="fas fa-undo-alt"></i>
                        </div>
                    </Tooltip>
                </div>
                {#if embeddingPrev.length > 0}
                    <div class="mx-2 numDisplay has-text-right" 
                        class:green={embeddingMeanDiff>0}
                        class:red={embeddingMeanDiff<0}
                        >
                        {embeddingMeanDiff.toFixed(2)}
                    </div>
                {/if}
            </div>
            <div class="sliderRow std">
                <Tooltip label="Std" position="is-bottom">
                    <div class="sliderIdx mr-1">σ</div>
                </Tooltip>
                <input type=range min={-1.5} max={1.5} step={0.01} value={valuesStd} on:change={setStd} />
                <div class="mx-2 numDisplay has-text-right">{valuesStd.toFixed(2)}</div>
                <div class="is-flex-grow-1">
                    <Tooltip label={valuesStd.toFixed(2)} position="is-left">
                        <div class="undo show mr-2"
                            on:click={() => resetEmbeddingAt()}>
                            <i class="fas fa-undo-alt"></i>
                        </div>
                    </Tooltip>
                </div>
                {#if embeddingPrev.length > 0}
                    <div class="mx-2 numDisplay has-text-right" 
                        class:green={embeddingStdDiff>0}
                        class:red={embeddingStdDiff<0}
                        >
                        {embeddingStdDiff.toFixed(2)}
                    </div>
                {/if}
            </div>
        </div>
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
        {#if embeddingPrev.length > 0}
            <div class="delStats flex-row">
                <div>
                    <Tag type="is-warning">δ stats</Tag>
                </div>
                <div class="flex-row">
                    <div class="mx-1 has-text-grey-light">µ</div>
                    <div class="mx-1">{embeddingDiffMean.toFixed(2)}</div>
                </div>
                <div class="flex-row">
                    <div class="mx-1 has-text-grey-light">σ</div>
                    <div class="mx-1">{embeddingDiffStd.toFixed(2)}</div>
                </div>
                <div class="flex-row">
                    <div class="mx-1 has-text-grey-light">L1</div>
                    <div class="mx-1">{embeddingDiffL1.toFixed(2)}</div>
                </div>
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
.delStats {
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
