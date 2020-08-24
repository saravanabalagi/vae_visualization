<script>
    export let image;
    export let title;
</script>

<div class="imageView">
    {#if image}
        <h2>{title}</h2>
        <img src={image} alt={title} />
    {/if}
</div>

<style>
    .imageView {
        padding: 10px;
    }
</style>
