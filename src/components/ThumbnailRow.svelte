<script>
  import { selectedImageStore } from '../searchQueryStore.js';
	import { BASE_URL } from '../searchengine.js';
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

	function handleDoubleClick(image) {
		console.log('handleDoubleClick', handleDoubleClick);
		let url = `${BASE_URL}webclient/img_detail/${image.id}`;
		window.open(url, '_blank').focus();
	}
</script>

{#each images as image (image.id)}
	<div class="studyThumb" class:selected={selectedImage?.id == image.id}>
		<a
			aria-label="Image: {image.name}"
			target="_blank"
			href="{BASE_URL}webclient/img_detail/{image.id}"
			on:click|preventDefault={() => handleClick(image)}
			on:dblclick={() => handleDoubleClick(image)}
		>
			<img src="{BASE_URL}webclient/render_thumbnail/{image.id}/" alt={image.name} />
		</a>
	</div>
{/each}
<span class="imgIndex">{index}</span>

<style>
	.studyThumb {
		display: inline-block;
		width: var(--thumbSize);
		height: var(--thumbSize);
		margin: 5px;
		padding: 0;
		position: relative;
		background-color: #ddd;
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
