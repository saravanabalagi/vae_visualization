<script>
    import ImageView from './ImageView.svelte';
    import {inputImage as inputImageStore} from './stores';
    let inputImage;
    const unsubscribeMod =  inputImageStore.subscribe(val => inputImage = val);
</script>

<div>
    <h2>Input</h2>
    <ImageView image={inputImage} />
</div>