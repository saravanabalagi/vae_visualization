<script>
    import {inputImage, inputImageFile} from './stores';

    let files;
    let image;
    function onFileUpload(e) {
        if(files && files[0]) {
            let reader = new FileReader();
            reader.onload = (ev) => {
                inputImage.set(ev.target.result);
                inputImageFile.set(files[0]);
            }
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
