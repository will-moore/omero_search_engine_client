<script>
	import { debounce } from '../util.js';
  import { getAutoCompleteResults, loadKnownKeys } from '../searchengine.js';
	import { onMount } from 'svelte';

  import AutocompleteItem from '../AutocompleteItem.svelte';

  import { queryStore } from '../searchQueryStore.js';

	let results = [];

  let filters = [];

  queryStore.subscribeAndFilters(newFilters => {
    console.log("newFilters", newFilters);
    filters = newFilters;
  })

	let loading = false;

  // Known keys loaded on mount
  let knownKeys = {project: [], image: []};
  let searchKey = 'Any';
  let operator = 'equals';

  onMount(() => {
    loadKnownKeys().then(r => {
      knownKeys = r;
      console.log('Known keys', knownKeys);
    });
  });


	let handleKeyup = (event) => {
		const query = event.target.value;
		loading = true;
		console.log('Searching for', query);
    let allKnownKeys = knownKeys.project.concat(knownKeys.image);
		getAutoCompleteResults(searchKey, query, allKnownKeys, operator).then(r => {
      loading = false;
      console.log('Results', r);
      results = r;
    });
	};
</script>

<h1>omero-searcher</h1>

Filters:

{#each filters as f}
  <p>Filter: {f.key} {f.value}</p>
{/each}

{searchKey}
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

Results: {results.length}
{#if results.length > 0}
	<h2>Results</h2>
	<ul>
		{#each results as result}
      <li><AutocompleteItem result={result} /></li>
		{/each}
	</ul>
{/if}

<style>
	.kvp_row {
    width: 500px;
		display: flex;
		flex-direction: row;
		margin-bottom: 1em;
    gap: 10px;
	}
</style>
