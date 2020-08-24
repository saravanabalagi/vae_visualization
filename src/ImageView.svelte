<script>
    export let image;
    export let title;
    export let loading;
</script>

<div class="imageView">
    <h2>{title}</h2>
    {#if loading != null && loading === true}
        <span>Loading</span>
    {:else if image}
        <img src={image} alt={title} />
    {:else}
        <span>No image loaded</span>
    {/if}
</div>

<style>
    .imageView {
        padding: 10px;
    }
</style>
