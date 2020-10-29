<script>
	import Embedding from './embeddings/Embedding.svelte';
	import OutputImageView from './images/OutputImageView.svelte';
	import InputImageView from './images/InputImageView.svelte';
	import ImageGrid from './images/ImageGrid.svelte';
	import VideoView from './videos/VideoView.svelte';
	import {inputImageFile, selectedServerImgIndex} from 'stores';
	import {Tabs, Tab} from 'svelma';

	import 'bulma/css/bulma.css';
	import '@fortawesome/fontawesome-free/css/all.css';
	import './main.css'
</script>

<div class="app">
	<ImageGrid />
	<div class="mainView container p-3">
		<Tabs>
			<Tab label="Image">
				<div class="ml">
					<InputImageView />
					{#if $inputImageFile != null || $selectedServerImgIndex != null}
						<Embedding />
						<OutputImageView />
					{/if}
				</div>
			</Tab>
			<Tab label="Video">
				<div class="video">
					<InputImageView />
					{#if $inputImageFile != null || $selectedServerImgIndex != null}
						<VideoView />
					{/if}
				</div>
			</Tab>
		</Tabs>
	</div>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		height: 100%;
	}
	.mainView {
		flex: 1;
		width: 100%;
	}
	.ml, .video {
		display: flex;
		flex-direction: row;
	}
</style>
