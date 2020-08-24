<script>
    let numbers = Array(10).fill(0);
    let values = Array.from(numbers);
</script>

<div class="embeddingView">
    <h2>Embedding</h2>
    {#each numbers as number, i}
        <div>
            <span>{number}</span>
            <input type=range min={-1} max={1} step={0.1} bind:value={values[i]} />
            <span class="numDisplay">{values[i]}</span>
        </div>
    {/each}
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
