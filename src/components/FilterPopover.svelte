<script>
  import { debounce } from '../util.js';
  import { getAutoCompleteResults, loadKnownKeys } from '../searchengine.js';
  import { onMount } from 'svelte';

  import AutocompleteList from './AutocompleteList.svelte';

  import { queryStore } from '../searchQueryStore.js';
  import FilterPopoverRight from './FilterPopoverRight.svelte';

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

    // When user closes the popover, we need to reset the filterIndex
    popover.addEventListener('toggle', (event) => {
      console.log('Popover toggled', event);
      if (event.newState == 'closed') {
        filterIndex = -1;
        queryStore.editFilter(-1);
      }
    });

    queryStore.subscribeFilterBeingEdited((idx) => {
      console.log('FilterPopover Editing filter', idx);
      filterIndex = idx;
      if (filterIndex != -1 && popover) {
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
    result.operator = operator;
    filterIndex = queryStore.addFilter(result);
  }

  function hidePopover() {
    popover.hidePopover();
  }
</script>

<div bind:this={popover} id="add-filter-dialog" popover>
  <button class="close" title="Close" on:click={hidePopover}>&times;</button>
  <div class="popover_content">
    <div class="left_panel">
      <h2>Add Filter</h2>

      <div class="kvp_row">
        <select bind:value={searchKey}>
          <option value="Any">Any Key</option>
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
        <input
          type="text"
          on:keyup={debounce(handleKeyup, 500)}
          placeholder="type to find values..."
        />
      </div>
      {#if loading}
        <p>Loading...</p>
      {/if}

      <div class="matches">
        <AutocompleteList handleClick={handleAutocompleteClick} items={results} />
      </div>
    </div>
    <div class="right_panel">
      <FilterPopoverRight />
    </div>
  </div>
</div>

<style>
  .matches {
    height: 100%;
    overflow-y: auto;
  }
  .kvp_row {
    width: 100%;
    display: flex;
    flex-direction: row;
    margin-bottom: 1em;
    gap: 10px;
  }
  .kvp_row select {
    flex: 34% 1 1;
  }
  .kvp_row input {
    flex: 66% 1 1;
  }
  #add-filter-dialog {
    width: 50%;
    min-width: 900px;
    height: 70%;
    overflow: auto;
    box-shadow: 5px 4px 10px -5px #737373;
    margin: auto;
    /* margin-bottom: 50px; */
    border: solid 1px black;
    border-radius: 10px;
  }
  .popover_content {
    width: 100%;
    height: 100%;
    max-width: 100%;
    padding: 15px;
    display: flex;
    flex-direction: row;
  }
  .left_panel,
  .right_panel {
    overflow: auto;
  }
  .left_panel {
    flex: 60% 0 0;
    padding-right: 15px;
  }
  .right_panel {
    flex: 40% 0 0;
    border-left: solid 1px #eee;
    padding-left: 15px;
  }
  .close {
    position: absolute;
    right: 5px;
    top: 5px;
    z-index: 100;
    font-size: 2rem;
    padding: 1px 9px 2px;
    line-height: 1.2;
    border: solid 1px #ddd;
    border-radius: 5px;
    background: #f9f9f9;
  }
</style>
