<script>
    import FileUpload from "./FileUpload.svelte";
    import ServerImagesImageView from "./ServerImagesImageView.svelte";

    let min = 0, max;
    const indexRangePromise = getIndexRange();
    async function getIndexRange() {
        const url = '/images'
        const res = await fetch(url);
        const resJson = await res.json();
        ({min, max} = resJson);
        return resJson;
    }

    const numImages = 20;
    const numRows = 2;
    $: numColumns = Math.ceil(numImages / numRows);
    $: randomIndices = getRandomIndices(numImages, min, max);

    function getRandomIndices(numImages, min, max) {
        return Array.from({length: numImages}, 
                            () => Math.floor(Math.random() * (max+1 - min) + min));
    }

    function randomize() {
        randomIndices = getRandomIndices(numImages, min, max);
    }
</script>

{#await indexRangePromise}
    Loading...
{:then range}
    <!-- {#if randomIndices.length > 0} -->
        <div class="serverImages">
            {#each Array.from(Array(numColumns).keys()) as c, i}
                <div class="column" idx={c} style="--maxWidth:{100/numColumns + '%'}">
                    {#each randomIndices.slice(c*numRows, c*numRows+numRows) as idx, j}
                        <ServerImagesImageView {idx} />
                    {/each}
                </div>
            {/each}
            <div>
                <FileUpload />
                <div on:click={randomize}>Randomize</div>
            </div>
        </div>
    <!-- {/if} -->
{/await}

<style>
    .serverImages {
        display: flex;
        flex-wrap: wrap;
    }
    .column {
        flex: var(--maxWidth);
        max-width: var(--maxWidth);
    }
</style>