<script>
	import { on } from 'svelte/events';
	import FilterPopover from '../components/FilterPopover.svelte';
	import { queryStore } from '../searchQueryStore.js';

	let filters = [];
  let editedFilter = -1;

	queryStore.subscribeFilters((newFilters) => {
		console.log('newFilters', newFilters);
		filters = newFilters;
    // editedFilter = queryStore.getFilterBeingEdited();
	});
  queryStore.subscribeFilterBeingEdited((filterIndex) => {
    editedFilter = filterIndex;
  })
</script>

<h1>omero-search-engine-client 2</h1>

Filters:
<button popovertarget="add-filter-dialog">Add</button>

<FilterPopover />

{#each filters as filterList, index}
	<p class:edited={editedFilter == index}>
		{#each filterList as f}
			<span class="or_filter">{f.key} {f.value} {f.active ? 'Y' : 'N'}</span>
		{/each}
		<label
			><input
				type="checkbox"
				title="Toggle Filter"
				on:change={() => queryStore.toggleFilter(index)}
			/>Disable</label
		>
		<button title="Remove Filter" on:click={() => queryStore.removeFilter(index)}>&times;</button>
		<button title="Edit Filter" on:click={() => queryStore.editFilter(index)}>Edit</button>
	</p>
{/each}

<style>
  .edited {
    border: solid red 1px;
  }
	.or_filter {
		background-color: #f0f0f0;
		padding: 0.2em;
		margin: 0.2em;
		border: solid grey 1px;
	}
</style>
