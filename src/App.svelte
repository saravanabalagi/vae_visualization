<script>
	import FileUpload from './FileUpload.svelte';
	import Embedding from './Embedding.svelte';
	import OutputImageView from './OutputImageView.svelte';
	import InputImageView from './InputImageView.svelte';
	
	let inputImageFile;
	import {inputImageFile as inputImageFileStore} from './stores';
	const unsubscribeInputImageFile =  inputImageFileStore.subscribe(val => inputImageFile = val);
</script>

<div class="app">
	<FileUpload />
	<div class="ml">
		<InputImageView />	
		{#if inputImageFile}
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
