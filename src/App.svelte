<script>
	import FileUpload from './FileUpload.svelte';
	import Embedding from './Embedding.svelte';
	import ImageView from './ImageView.svelte';
	let inputImage;
	let outputImage;

	function setInputImage(img) { inputImage = img; sendInputImageToServer(); }
	async function sendInputImageToServer() {
		const content = {
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({hello: 'world'})
		};
		const url = 'http://localhost:5000/hello_post';
		const response = await fetch(url, content);
		const json = await response.json();
		console.log({json});
	}
</script>

<div class="app">
	<FileUpload setInputImage={setInputImage} />
	<div class="ml">
		<ImageView title="Input" image={inputImage} />
		<Embedding />
		<ImageView title="Output" image={inputImage} />
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
