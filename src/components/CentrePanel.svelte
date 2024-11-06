<script>
	import { get } from 'svelte/store';
	import { queryStore, selectedContainerStore, selectedImageStore } from '../searchQueryStore.js';
	import { BASE_URL, submitSearch } from '../searchengine.js';

	let selectedImage = null;

	let imagesJson = [];

	let total_pages = 1;
	let pagination = null;

  // if either the filters or the selected container changes, we need to reload the images
	queryStore.subscribeFilters((newFilters) => {
		loadImages();
	});
	selectedContainerStore.subscribe((obj_id) => {
		loadImages();
	});
	async function loadImages() {
		let obj = get(selectedContainerStore);
		if (!obj) {
			imagesJson = [];
			return;
		}
		let query = queryStore.getQuery(obj.name);
		let data = await submitSearch(query);
		imagesJson = data.results.results;

		// Store pagination info...
		total_pages = data.results.total_pages;
		pagination = data.results.pagination;
		// TODO: To load next page of images, we can just do
		// query.pagination = pagination;
	}

  function handleClick(image) {
    selectedImage = image;
    selectedImageStore.set(image);
  }
</script>

<ul>
	{#each imagesJson as image}
		<li class="studyThumb" class:selected={selectedImage?.id == image.id}>
			<a
				aria-label="Image: {image.name}"
				target="_blank"
				href="{BASE_URL}webclient/img_detail/{image.id}"
				on:click|preventDefault={() => handleClick(image)}
			>
				<img
					alt="Thumbnail for {image.name}"
					title={image.name}
					src="{BASE_URL}webclient/render_thumbnail/{image.id}/"
					loading="lazy"
				/>
			</a>
		</li>
	{/each}
</ul>

<style>
	ul {
		padding: 15px;
	}
	.studyThumb {
		display: inline-block;
		width: 64px;
		height: 64px;
		margin: 1px;
		padding: 0;
		position: relative;
		background-color: #ddd;
	}
	.studyThumb img {
		max-width: 100%;
		height: auto;
		display: inline-block;
		vertical-align: middle;
	}
  .selected img {
    border: 4px solid #3875d7;
  }
</style>
