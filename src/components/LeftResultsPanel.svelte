<script>
  import { onMount } from 'svelte';

  import { queryStore, selectedContainerStore } from '../searchQueryStore.js';
  import { submitSearch } from '../searchengine.js';

  import folder16png from '../lib/assets/folder16.png';
  import folderScreen16png from '../lib/assets/folder_screen16.png';

  let resultContainers = [];
  let selectedContainer = null;

  let controller = new AbortController();

  queryStore.subscribeFilters((newFilters) => {
    // This is called when filters change AND when we initially subscribe
    let query = queryStore.getQuery();
    console.log('SEARCHING....', query);
    doSearch(query);
  });
  // When the selected container changes (e.g. click below OR history back/foward)
  // we need to update the filters
  selectedContainerStore.subscribe((container) => {
    selectedContainer = container;
  });

  async function doSearch(query) {
    // abort any previous requests...
    controller.abort();
    controller = new AbortController();
    let containers = true;
    let data = await submitSearch(query, containers, {signal: controller.signal});
    console.log('Search result', data);
    // sort results by name
    data.results.results.sort((a, b) => a.name.localeCompare(b.name));
    resultContainers = data.results.results;

    // If we have selectedContainer (e.g. from URL), need to set the name so it can be used for
    // center panel query (URL only gives us the id and type)
    if (selectedContainer && !selectedContainer.name) {
      let container = resultContainers.find((c) => c.id == selectedContainer.id && c.type == selectedContainer.type);
      if (container) {
        // add a flag to ignore the right panel
        selectedContainerStore.set({...container, ignoreRightPanel: true});
      }
    }
  }

  function handleClick(container) {
    console.log('Clicked', container);
    selectedContainerStore.set(container);
  }
</script>

<div class="scrollable">
  <ul>
    {#each resultContainers as container}
      <li class:selected={container.id == selectedContainer?.id && container.type == selectedContainer?.type}>
          <div class="container_icon">
          <img
            alt="Container icon"
            src={container.type == 'screen' ? folderScreen16png : folder16png}
          />
          </div>
          <button onclick={() => handleClick(container)} class="container_text">
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
    width: fit-content;
    margin: 3px;
  }
  .selected {
    background-color: #B3BDCC;
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
