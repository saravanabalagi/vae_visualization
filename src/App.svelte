<script>
	import FileUpload from './FileUpload.svelte';
	import Embedding from './Embedding.svelte';
	import ImageView from './ImageView.svelte';
	export let name;
	let inputFile;
	let inputImage;
	let outputImage;
	let loading = false;

	function setInputImage(img, iFile) { 
		inputImage = img;
		inputFile = iFile;
		sendInputImageToServer(); 
	}

	async function sendInputImageToServer() {
		loading = true;
		const data = new FormData();
		data.append('file', inputFile)
		const content = {
			method: 'POST',
			body: data
		};
		const url = '/upload';
		outputImage = await fetch(url, content);
		const response = await fetch(url, content);

		// display blob image https://stackoverflow.com/a/43871843/3125070
		const urlCreator = window.URL || window.webkitURL;
		outputImage = urlCreator.createObjectURL(await response.blob());
		loading = false;
	}
</script>

<div class="app">
	<FileUpload setInputImage={setInputImage} />
	<div class="ml">
		<ImageView title="Input" image={inputImage} />
		<Embedding />
		<ImageView title="Output" image={outputImage} loading={loading} />
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
