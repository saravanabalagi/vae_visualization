<script>
    export let setInputImage;
    let files;
    let image;
    function onFileUpload(e) {
        if(files && files[0]) {
            let reader = new FileReader();
            reader.onload = (ev) => setInputImage(ev.target.result, files[0]);
            reader.readAsDataURL(files[0]);
        }
    }

</script>

<input type="file" bind:files accept="image/*" on:change={onFileUpload}>

<div>
    {#if files && files[0]}
        <p>
            {files[0].name}
        </p>
    {/if}
</div>
