<script>
import { Tag } from 'svelma';
import { slide } from 'svelte/transition';

export let image;
export let advanced = false;

let widthNatural, heightNatural;
let scale = 1;
let custom = false;

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
        <div class="quickScales">
            {#each [1,2,3,4] as s}
                <div class="mx-1" on:click={() => { scale = s; custom = false; }}><Tag type={scale==s?'is-info':'is-none'}>{s}x</Tag></div>
            {/each}
            <div class="mx-1" on:click={() => custom = true}><Tag type={custom?'is-info':'is-none'}>custom</Tag></div>
        </div>
        {#if custom}
            <div transition:slide class="m-1">
                Scale: 
                <input class="scaleInput" type="number" bind:value={scale} step={0.1} max={9.9} min={0.1}>
                x
            </div>
        {/if}
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
.quickScales {
    cursor: pointer;
    user-select: none;
    display: flex;
}
</style>
