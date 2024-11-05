<script>
	import { debounce } from '../util.js';
	import { getAutoCompleteResults, loadKnownKeys } from '../searchengine.js';
	import { onMount } from 'svelte';

	import AutocompleteItem from '../AutocompleteItem.svelte';

	import { queryStore } from '../searchQueryStore.js';

	// The Index of the filter being edited. -1 means we are creating a new filter.
	// When we click on an autocomplete item, we will add a filter to the queryStore and update this index.
	export let filterIndex = -1;
	let results = [];

	let loading = false;

	// Known keys loaded on mount
	let knownKeys = { project: [], image: [] };
	let searchKey = 'Any';
	let operator = 'equals';
	let popover;

	onMount(() => {
		loadKnownKeys().then((r) => {
			knownKeys = r;
			console.log('Known keys', knownKeys);
		});

		popover.addEventListener('toggle', (event) => {
			console.log('Popover toggled', event);
			if (event.newState == "closed") {
				queryStore.editFilter(-1);
			}
		});

		queryStore.subscribeFilterBeingEdited((filterIndex) => {
			console.log('FilterPopover Editing filter', filterIndex);
			if (filterIndex != -1) {
				popover.showPopover();
			}
		});
	});

	let handleKeyup = (event) => {
		const query = event.target.value;
		loading = true;
		console.log('Searching for', query);
		let allKnownKeys = knownKeys.project.concat(knownKeys.image);
		getAutoCompleteResults(searchKey, query, allKnownKeys, operator).then((r) => {
			loading = false;
			console.log('Results', r);
			results = r;
		});
	};

	function handleAutocompleteClick(result) {
		console.log('FilterPopover Adding filter', result);
		filterIndex = queryStore.addFilter(result);
	}
</script>

<div bind:this={popover} id="add-filter-dialog" popover>
	<h2>{filterIndex == -1 ? 'Add Filter' : `Edit Filter: ${filterIndex}`}</h2>

	<div class="kvp_row">
		<select bind:value={searchKey}>
			<option value="Any">Any</option>
			<optgroup label="Study">
				{#each knownKeys.project as key}
					<option value={key}>{key}</option>
				{/each}
			</optgroup>
			<optgroup label="Image">
				{#each knownKeys.image as key}
					<option value={key}>{key}</option>
				{/each}
			</optgroup>
		</select>
		<select bind:value={operator}>
			<option value="contains">contains</option>
			<option value="equals">equals</option>
		</select>
		<input type="text" on:keyup={debounce(handleKeyup, 500)} placeholder="Search IDR" />
	</div>
	{#if loading}
		<p>Loading...</p>
	{/if}

	<div class="matches">
		<ul>
			{#each results as result}
				<li><AutocompleteItem {result} handleClick={handleAutocompleteClick} /></li>
			{/each}
		</ul>
	</div>
</div>

<style>
	.matches {
		height: 300px;
		max-height: 300px;
		overflow-y: auto;
	}
	.kvp_row {
		width: 500px;
		display: flex;
		flex-direction: row;
		margin-bottom: 1em;
		gap: 10px;
	}
	#add-filter-dialog {
		width: 50%;
		height: 50%;
		overflow: auto;
		box-shadow: 5px 4px 10px -5px #737373;
  }
</style>
