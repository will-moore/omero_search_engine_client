<script>
  import Fa from 'svelte-fa';
  import { faBan, faTrash } from '@fortawesome/free-solid-svg-icons';
	import { queryStore } from '../searchQueryStore.js';

	let filters = [];
	let filterIndex = -1;

	queryStore.subscribeFilters((newFilters) => {
		filters = newFilters;
	});

	queryStore.subscribeFilterBeingEdited((idx) => {
		filterIndex = idx;
	});

  function handleOperatorChange(or_index, event) {
    console.log('Operator change', or_index, event.target.value);
    queryStore.updateFilterOperator(filterIndex, or_index, event.target.value);
  }
</script>

<!-- FilterIndex: {filterIndex} <br>
			Filters: {filters.length} <br> 
Filters at idx: {JSON.stringify(filters[filterIndex])} -->

{#if filters[filterIndex]}
  <h2>Edit Filters</h2>
	{#each filters[filterIndex] as f, or_index}
    {#if or_index > 0}
      <span>or</span>
    {/if}
		<div class="or_filter">
      <div class="keyvalue" class:active={f.active}>
			{f.name}
			<select bind:value={f.operator} onchange={(event) => handleOperatorChange(or_index, event)}>
				<option value="equals">equals</option>
				<option value="contains">contains</option>
			</select>
			{f.value}{f.operator == "contains" ? "*" : ""}
      </div>

      <div class="filter_buttons">
        <button title="Disable filter" onclick={() => queryStore.toggleOrFilter(filterIndex, or_index)}>
          <Fa icon={faBan} color="#666" />
        </button>
        <button title="Remove Filter" onclick={() => queryStore.removeOrFilter(filterIndex, or_index)}>
          <Fa icon={faTrash} color="#666" />
        </button>
      </div>
		</div>
	{/each}
{/if}


<style>
  .or_filter {
    display: flex;
    flex-direction: row;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin: 5px;
  }
  .keyvalue {
    flex: auto 1 1;
    opacity: 0.3;
  }
  .keyvalue.active {
    opacity: 1;
  }
  .filter_buttons {
    flex: 0 0 auto;
    display: flex;
    flex-direction: row;
  }
  button {
    border: none;
    background: none;
    cursor: pointer;
  }

  .or_filter select {
    margin: 0 5px;
  }
</style>