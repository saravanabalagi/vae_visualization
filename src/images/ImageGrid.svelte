<script>
import FileUpload from "../files/FileUpload.svelte";
import ServerImage from "./ServerImage.svelte";
import { Button } from 'svelma';

let folders = [];
const indexRangePromise = getImgFolders();
async function getImgFolders() {
    const url = '/images'
    const res = await fetch(url);
    const resJson = await res.json();
    folders = resJson.files;
    return resJson;
}

const numImages = 20;
const numRows = 2;
$: numColumns = Math.ceil(numImages / numRows);
$: randomIndices = getRandomIndices(numImages, 0, folders.length-1);
const loadingImages = Array(numImages).fill(false);

function getRandomIndices(numImages, min, max) {        // min max inclusive
    return Array.from({length: numImages}, 
                        () => Math.floor(Math.random() * (max+1 - min) + min));
}

function randomize() { randomIndices = getRandomIndices(numImages, 0, folders.length-1); }
function setLoading(idx, loadingBool) { loadingImages[idx] = loadingBool; }
</script>

{#await indexRangePromise}
    Loading...
{:then range}
    <div class="custom-grid-wrapper">
        <div class="custom-grid">
            {#each Array.from(Array(numColumns).keys()) as c, i}
                <div class="custom-grid-column" idx={c} style="--maxWidth:{100/numColumns + '%'}">
                    {#each randomIndices.slice(c*numRows, c*numRows+numRows) as idx, j}
                        <ServerImage imgDir={folders[idx]} setLoading={(loadingBool) => setLoading(idx, loadingBool)} />
                    {/each}
                </div>
            {/each}
        </div>
        <div class="button-row">
            <FileUpload />
            <Button type="is-danger" on:click={randomize} loading={loadingImages.some(e => e === true)}>Randomize</Button>
        </div>
    </div>
{/await}

<style>
.custom-grid-wrapper {
    display: flex;
}
.custom-grid {
    display: flex;
    flex-wrap: wrap;
}
.custom-grid-column {
    flex: var(--maxWidth);
    max-width: var(--maxWidth);
}
.button-row {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    padding: 10px;
    background-color: #333;
}
</style>
