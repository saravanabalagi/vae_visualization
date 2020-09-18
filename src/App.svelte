<script>
	import Embedding from './Embedding.svelte';
	import OutputImageView from './OutputImageView.svelte';
	import InputImageView from './InputImageView.svelte';
	import ImageGrid from './ImageGrid.svelte';
	import {inputImageFile, selectedServerImgIndex} from './stores';
</script>

<div class="app">
	<ImageGrid />
	<div class="ml">
		<InputImageView />	
		{#if $inputImageFile != null || $selectedServerImgIndex != null}
			<Embedding />
			<OutputImageView />
		{/if}
	</div>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
	}
	.ml {
		display: flex;
		flex-direction: row;
	}
</style>
