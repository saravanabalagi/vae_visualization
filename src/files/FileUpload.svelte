<script>
import { customImg } from '../stores';
import { imgIdx } from '../serverImgStores';
import { Button } from 'svelma';

let fileUploadElement;
let files;
function onFileUpload(e) {
    if(files && files[0]) {
        let reader = new FileReader();
        reader.onload = (ev) => {
            imgIdx.set(null);
            customImg.set(files[0]);
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
