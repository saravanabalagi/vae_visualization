<script>
    export let image;
</script>

<div class="imageView">
    {#if image}
        <img src={image} />
    {:else}
        <span>No image loaded</span>
    {/if}
</div>

<style>
    .imageView {
        padding: 10px;
    }
</style>
