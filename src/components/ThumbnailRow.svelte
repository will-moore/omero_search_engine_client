<script>
	import { selectedImageStore } from '../searchQueryStore.js';
	import { BASE_URL, OMERO_URL } from '../searchengine.js';
	import { onMount } from 'svelte';

	export let images = [];
	export let index = 0;
	export let handleRendered;

	let selectedImage = null;

	onMount(() => {
		handleRendered(index);
	});

	// selected image can change due to browser history or click below
	selectedImageStore.subscribe((image) => {
		selectedImage = image;
	});

	function handleClick(image) {
		selectedImageStore.set(image);
	}

	function handleDoubleClick(image_url) {
		window.open(image_url, '_blank').focus();
	}
</script>

{#each images as image (image.id)}
	{@const thumb_url =
		image?.key_values?.find((kvp) => kvp.name == 'thumb_url')?.value ||
		`${OMERO_URL}webclient/render_thumbnail/${image.id}/`}
  {@const image_url =
		image?.key_values?.find((kvp) => kvp.name == 'image_url')?.value ||
		`${OMERO_URL}webclient/img_detail/${image.id}/`}
	<a
		aria-label="Image: {image.name}"
		target="_blank"
		href={image_url}
		on:click|preventDefault={() => handleClick(image)}
		on:dblclick={() => handleDoubleClick(image_url)}
	>
		<div class="studyThumb" class:selected={selectedImage?.id == image.id}>
			<img src={thumb_url} alt={image.name} />
		</div>
	</a>
{/each}
<span class="imgIndex">{index}</span>

<style>
	.studyThumb {
		width: var(--thumbSize);
		height: var(--thumbSize);
		margin: 5px;
		padding: 0;
		position: relative;
		background-color: #ddd;
		/* align child img in centre */
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.studyThumb img {
		max-width: 100%;
		max-height: 100%;
		aspect-ratio: auto;
		height: auto;
		display: inline-block;
		vertical-align: middle;
	}
	.selected img {
		border: 4px solid #3875d7;
	}

	.imgIndex {
		color: #aaa;
	}
</style>
