<script>
    import { serverImgPath, customImg } from '../stores';
    import ImageView from "./ImageView.svelte";
    export let idx;
    export let setLoading;
    let imagePath;

    $: imagePathPromise = getImagePath(idx);
    async function getImagePath(idx) {
        setLoading(idx, true);
        const url = `/image_paths/${idx}`
        const res = await fetch(url);
        const resJson = await res.json();
        setLoading(idx, false);
        imagePath = resJson.path;
        return resJson.path;
    }

    function saveImgPathToStore() {
        customImg.set(null);
        serverImgPath.set(imagePath);
    }
</script>

<div class="serverImage" on:click={saveImgPathToStore}>
    {#if imagePath != null}
        <ImageView image={imagePath} />
    {/if}
</div>

<style>
.serverImage {
    cursor: pointer;
}

</style>
