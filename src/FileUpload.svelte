<script>
    import {inputImage, inputImageFile, selectedServerImgIndex} from './stores';
    import { Button } from 'svelma';

    let fileUploadElement;
    let files;
    function onFileUpload(e) {
        if(files && files[0]) {
            let reader = new FileReader();
            reader.onload = (ev) => {
                inputImage.set(ev.target.result);
                inputImageFile.set(files[0]);
                selectedServerImgIndex.set(null);
            }
            reader.readAsDataURL(files[0]);
        }
    }
</script>

<Button type="is-info" on:click={() => fileUploadElement.click()}>
    Upload Image
    <input bind:this={fileUploadElement} type="file" bind:files accept="image/*" on:change={onFileUpload}>
</Button>

<style>
    input[type="file"] {
        display: none;
    }
</style>