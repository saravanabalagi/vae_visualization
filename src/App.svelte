<script>
import Embedding from './embeddings/Embedding.svelte';
import OutputImageView from './images/OutputImageView.svelte';
import InputImageView from './images/InputImageView.svelte';
import ImageGrid from './images/ImageGrid.svelte';
import { Tag } from 'svelma';
import { routes, customImg } from './stores';
import { imgPath } from './serverImgStores';

import 'bulma/css/bulma.css';
import '@fortawesome/fontawesome-free/css/all.css';
import './main.css'

let promise = getRoutes();
async function getRoutes() {
    const url = '/paths';
	let response = await fetch(url);
    let responseJson = await response.json();
	console.debug('routes', responseJson);
	routes.set(responseJson);
}

let collapsed = false;
</script>

<div class="app">
	{#await promise}
		<i class="fas fa-circle-notch fa-spin has-text-info"></i>
		<div>
			Loading...
		</div>
	{:then response}
		<div class="topPanel" class:collapsed>
			<ImageGrid />
			<div class="flex-row mx-2 mt-2 is-justify-content-space-around">
				<div class="flex-row m-2">
					<div class="px-1"><Tag type="is-info">Model</Tag></div>
					<div class="px-1">{$routes.ckpt_path}</div>
				</div>
				<div class="flex-row m-2">
					<div class="px-1"><Tag type="is-info">Images</Tag></div>
					<div class="px-1">{$routes.img_dir_path}</div>
				</div>
			</div>
			<div class="toggleCollapse"
				class:collapsed 
				on:click={() => collapsed = !collapsed}>
				<i class="fas fa-chevron-circle-up"></i>
			</div>
		</div>
		<div class="mainView container p-3">
			<InputImageView />
			{#if $customImg != null || $imgPath != null}
				<Embedding />
				<OutputImageView />
			{/if}
		</div>
	{:catch error}
		<i class="fas fa-exclamation-triangle has-text-warning"></i>
		<div>
			{error}
		</div>
	{/await}
</div>

<style lang="scss">
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
.topPanel {
	position: relative;
	transition: all 300ms ease-in-out;
	&.collapsed {
		transform: translateY(-100%);
		position: absolute;
	}
	.toggleCollapse {
		transition: all 300ms ease-in-out;
		position: absolute;
		bottom: 0;
		left: 0;
		padding: 10px;
		cursor: pointer;
		&.collapsed {
			bottom: -40px;
			transform: rotateZ(180deg);
		}
	}
}
</style>
