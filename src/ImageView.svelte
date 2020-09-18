<script>
    export let image;
</script>

<div class="imageView">
    {#if image}
        <img src={image} alt="ImageView" />
    {:else}
        <span>No image loaded</span>
    {/if}
</div>

<style>
    .imageView img {
        width: 100%;
        display: block;
    }
</style>
