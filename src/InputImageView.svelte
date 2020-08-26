<script>
    import ImageView from './ImageView.svelte';
    import {inputImage} from './stores';
</script>

<div>
    <h2>Input</h2>
    <ImageView image={$inputImage} />
</div>