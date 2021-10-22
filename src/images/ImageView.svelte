<script>
export let image;
export let advanced = false;

let widthNatural, heightNatural;
let scale = 1;

const handleImageLoad = (e) => {
    const img = e.target;
    if (img == null) {
        widthNatural = heightNatural = 'undefined';
    }
	widthNatural = img.naturalWidth;
	heightNatural = img.naturalHeight;
}
</script>

<div class="imageView">
    {#if image}
        <img width={scale*widthNatural} height={scale*heightNatural} src={image} on:load={handleImageLoad} alt="ImageView" />
    {:else}
        <span>No image loaded</span>
    {/if}
</div>
{#if advanced}
    <div class="advanced m-2">
        <div class="info px-2 m-1">{widthNatural} x {heightNatural}</div>
        <div class="m-1">
            Scale: 
            <input class="scaleInput" type="number" bind:value={scale} step={0.1} max={9.9} min={0.1}>
            x
        </div>
    </div>
{/if}

<style>
.imageView img {
    margin: auto;
    display: block;
}
.advanced {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.scaleInput {
    width: 50px;
}
.info {
    text-align: center;
}
</style>
