<script>
import Embedding from './embeddings/Embedding.svelte';
import OutputImageView from './images/OutputImageView.svelte';
import InputImageView from './images/InputImageView.svelte';
import ImageGrid from './images/ImageGrid.svelte';
import { customImg } from './stores';
import { imgPath } from './serverImgStores'

import 'bulma/css/bulma.css';
import '@fortawesome/fontawesome-free/css/all.css';
import './main.css'
</script>

<div class="app">
	<ImageGrid />
	<div class="mainView container p-3">
		<InputImageView />
		{#if $customImg != null || $imgPath != null}
			<Embedding />
			<OutputImageView />
		{/if}
	</div>
</div>

<style>
.app {
	display: flex;
	flex-direction: column;
	height: 100%;
}
.mainView {
	display: flex;
	flex: 1;
	width: 100%;
}
</style>
