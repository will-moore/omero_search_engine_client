<script>
  import Fa from 'svelte-fa';
  import { faBan, faTrash, faPen } from '@fortawesome/free-solid-svg-icons';
  import JsonURL from "@jsonurl/jsonurl";
  // import { pushState } from '$app/navigation';

  import FilterPopover from '../components/FilterPopover.svelte';
  import Nav from '../components/Nav.svelte';
  import LeftResultsPanel from '../components/LeftResultsPanel.svelte';
  import RightPanel from '../components/RightPanel.svelte';
  import { queryStore } from '../searchQueryStore.js';
  import CentrePanel from '../components/CentrePanel.svelte';
  import { onMount } from 'svelte';

  let filters = $state([]);
  let editedFilter = $state(queryStore.getFilterBeingEdited());

  let ignoreFilterChange = false;

  function pushStateFilters() {
    if (ignoreFilterChange) {
      return;
    }
    let filterJson = queryStore.getFilters();
    // Prefer NOT to use URLSearchParams as it will encode the query string
    let url = window.location.pathname;
    if (filterJson.length > 0) {
      let query = JsonURL.stringify(filterJson, { AQF: true });
      url += `?query=${query}`;
    }
    // state can be used by onpopstate() to restore the filters on back/forward
    // URL is for users to share the link / refresh page.
    history.pushState({query: filterJson}, "", url);
  }

  function onpopstate(event) {
    let filterJson = event.state;
    console.log('popstate state', filterJson);
    ignoreFilterChange = true;
    if (filterJson.query) {
      queryStore.setFilters(filterJson.query);
    }
    setTimeout(() => {
      ignoreFilterChange = false;
    }, 100);
  }


  onMount(() => {
    console.log("onMount ---->");
    queryStore.subscribeFilters((newFilters) => {
      console.log('newFilters', newFilters);
      filters = newFilters;
      pushStateFilters();
    });
    queryStore.subscribeFilterBeingEdited((filterIndex) => {
      editedFilter = filterIndex;
    });
  });

  // BEFORE the page is mounted, we need to check the URL for any query parameters
  const paramsString = window.location.search.slice(1);
  const searchParams = new URLSearchParams(paramsString)
  let query = searchParams.get("query");
  console.log("URLSearchParams query:", query);
  if (query) {
    // we actually need to encode the query string for JsonURL to work
    let filterJson = JsonURL.parse(encodeURIComponent(query), { AQF: true });
    console.log("URLSearchParams filterJson...", filterJson);
    if (filterJson?.length > 0) {
      queryStore.setFilters(filterJson);
    }
  } else {
    // check for e.g. ?key=Gene+Symbol&value=pax7&operator=equals
    let key = searchParams.get("key");
    let value = searchParams.get("value");
    let operator = searchParams.get("operator") || "equals";
    console.log("URLSearchParams key:", key, "value:", value, "operator:", operator);
    if (key && value) {
      queryStore.addFilter({ key: key, value: value, dtype: "image", operator: operator });
    }
  }
  
</script>

<svelte:window {onpopstate} />

<Nav />

<FilterPopover />

<div class="main">
  <div class="sidebar">
    <div class="filter_panel">
    <h3>
      Studies
      <button class="addBtn" popovertarget="add-filter-dialog">Add Filter</button>
    </h3>
    {#each filters as filterList, index}
      {@const uniqueKeys = Array.from(new Set(filterList.map((f) => f.name)))}
      <div class="and_filter" class:edited={editedFilter == index}>
        <div class="filter_content">
          {#if uniqueKeys.length == 1}
            <strong>{uniqueKeys[0]}:</strong>
          {/if}
          {#each filterList as f, idx}
            {#if idx > 0}
              <span>or</span>
            {/if}
            <button on:click={() => queryStore.toggleOrFilter(index, idx)} class="or_filter" class:active={f.active} title="{f.name} {f.operator} {f.value}">
              {#if uniqueKeys.length > 1}
                <strong>{f.name}:</strong>
              {/if}
              {f.value}{f.operator == "contains" ? "*" : ""}
            </button>
          {/each}
        </div>

        <div class="filter_buttons">
          <button title="Edit Filters" on:click={() => queryStore.editFilter(index)}>
            <Fa icon={faPen} color="#666" />
          </button>
          <button title="Disable filter" on:click={() => queryStore.toggleFilter(index)}>
            <Fa icon={faBan} color="#666" />
          </button>
          <button title="Remove Filter" on:click={() => queryStore.removeFilter(index)}
            ><Fa icon={faTrash} color="#666" /></button
          >
        </div>
      </div>
    {/each}
      </div>
      <!-- Show Projects and Screens -->
      <div class="container_panel">
        <LeftResultsPanel />
      </div>
  </div>

  <div class="content">
    <CentrePanel />
  </div>
  <div class="sidebar">
    <RightPanel />
  </div>
</div>

<style>
  .main {
    flex: auto 1 1;
    display: flex;
    flex-direction: row;
    width: 100%;
    background: #f1f0f4;
  }
  .sidebar {
    flex: 0 0 400px;
    margin: 10px;
    display: flex;
    flex-direction: column;
  }
  .container_panel {
    flex: auto 1 1;
    overflow: auto;
    /* larger content pushes it higher, but at least we get a scrollbar */
    height: 300px;
  }
  .content {
    flex: auto 1 1;
    border: solid #ddd 1px;
    border-width: 0 1px;
    background-color: white;
    overflow: auto;
  }
  h3 {
    margin-bottom: 10px;
  }
  .addBtn {
    float: right;
    padding: 4px 12px;
    font-size: 14px;
    border: 0;
    background-color: var(--button-bg);
    color: var(--button-color);
    border-radius: 5px;
    cursor: pointer;
  }
  .and_filter {
    border: solid lightgray 1px;
    border-radius: 5px;
    padding: 5px;
    font-size: 14px;
    margin-bottom: 7px;
    background-color: white;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .filter_content {
    flex: auto 1 1;
  }
  .filter_buttons {
    display: flex;
    flex-direction: row;
    flex: 0 0 auto;
    padding: 4px 3px;
    height: fit-content;
  }
  .filter_buttons button {
    border: none;
    background-color: transparent;
  }
  .edited {
    border: solid black 1px;
  }
  .or_filter {
    background-color: #f0f0f0;
    padding: 2px 5px;
    margin: 1px 3px 1px 0;
    border: solid rgb(177, 175, 175) 1px;
    border-radius: 5px;
    display: inline-block;
    opacity: 0.4;
  }
  .active {
    opacity: 1;
  }
  strong {
    font-weight: 600;
  }
</style>
