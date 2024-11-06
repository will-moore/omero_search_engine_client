<script>
	import { onMount } from 'svelte';

	import { queryStore } from '../searchQueryStore.js';
	import { submitSearch } from '../searchengine.js';

	import folder16png from '../lib/assets/folder16.png';
	import folderScreen16png from '../lib/assets/folder_screen16.png';

	let resultContainers = [];

	onMount(() => {
		console.log('LeftResultsPanel mounte - Initial Search...');
		doSearch(queryStore.getQuery());
	});

	queryStore.subscribeFilters((newFilters) => {
		let query = queryStore.getQuery();
		console.log('SEARCHING....', query);
		doSearch(query);
	});

	async function doSearch(query) {
		let data = await submitSearch(query);
		console.log('Search result', data);
		// sort results by name
		data.results.results.sort((a, b) => a.name.localeCompare(b.name));
		resultContainers = data.results.results;
	}

  function handleClick(container) {
    console.log('Clicked', container);

  }
</script>

<div class="scrollable">
	<ul>
		{#each resultContainers as container}
			<li>
          <div class="container_icon">
					<img
						alt="Container icon"
						src={container.type == 'screen' ? folderScreen16png : folder16png}
					/>
          </div>
					<button on:click={() => handleClick(container)} class="container_text">
						{container.name}
						<span class="children_count">{container['image count']}</span>
					</button>
			</li>
		{/each}
	</ul>
</div>

<style>
	.scrollable {
		overflow-y: auto;
	}
	ul,
	li {
		list-style: none;
		padding: 0;
		font-size: 13px;
		color: rgba(61, 71, 92, 0.9);
		font-family: 'HelveticaNeue-Medium', Helvetica, Arial, sans-serif;
	}
	li {
		display: flex;
		flex-direction: row;
    gap: 1px;
		width: 100%;
    margin: 3px;
	}
  .container_icon {
    flex: 0 0 auto;
    width: 20px;
    height: 20px;
  }
  .container_icon img {
    margin: 3px 0;
  }
  .container_text {
    flex: auto 1 1;
    border: none;
    background-color: transparent;
    font: inherit;
    cursor: pointer;
    color: inherit;
    text-align: left;
    margin: 0;
    padding: 0;
  }
	.children_count {
		opacity: 0.6;
		background-color: rgba(0, 0, 0, 0.05);
		border-radius: 2px;
		display: inline-block;
		padding: 0 3px;
	}
</style>
