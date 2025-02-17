<script>
  import { get } from 'svelte/store';
  import { fade } from 'svelte/transition';
  import VirtualList from 'svelte-tiny-virtual-list';

  import { queryStore } from '../searchQueryStore.js';
  import { selectedContainerStore } from '../containerStore.js';
  import { submitSearch } from '../searchengine.js';
  import ThumbnailRow from './ThumbnailRow.svelte';
  import { onMount } from 'svelte';
  import { addKeyValueQuery } from '../searchengine.js';

  export let parentQuery = undefined;
  export let setPrototypeImage = undefined;

  // NB: THUMB_SIZE is also defined in ThumbnailRow.svelte
  const THUMB_SIZE = 64;
  
  let panelHeight = 0;
  let panelWidth = 0;

  let imagesJson = [];
 
  // re-calculated based on panelWidth
  $: thumbColumns = 7;

  let pagination = null;
  let controller;
  let loading = false;

  // if either the filters or the selected container changes, we need to reload the images
  queryStore.subscribeFilters((newFilters) => {
    console.log("Images.svelte::: queryStore newFilters - parentQuery:", parentQuery)
    loadImages();
  });
  selectedContainerStore.subscribe((obj_id) => {
    console.log("Images.svelte::: selectedContainerStore newFilters - parentQuery:", parentQuery)
    loadImages();
  });

  async function loadImages(clear = true) {

    let obj = get(selectedContainerStore);
    if (!obj?.name) {
      imagesJson = [];
      pagination = null;
      return;
    }
    let baseQuery = {};
    if (parentQuery == undefined) {
      console.log('loadImages... parentQuery is undefined');
      baseQuery = queryStore.getQuery();
    } else {
      // deepcopy the parentQuery
      baseQuery = JSON.parse(JSON.stringify(parentQuery));
    }
    let query = addKeyValueQuery(baseQuery, "name", obj.name, "container");
    if (!clear && pagination) {
      if (pagination.current_page >= pagination.total_pages) {
        return;
      }
      // include pagination so we get the next page...
      query.pagination = pagination;
    }
    if (controller) {
      controller.abort();
    }
    console.log('loadImages... query', query, clear);
    loading = true;
    controller = new AbortController();
    let data = await submitSearch(query, false, { signal: controller.signal });

    // Store pagination info...
    // total_pages = data.results.total_pages;
    pagination = data.results.pagination;

    loading = false;
    let resultImages = data.results?.results || [];
    if (resultImages.length == 0) {
      console.log("NO IMAGES FOUND!", query);
    }
    if (clear) {
      // replace the existing images
      imagesJson = resultImages;
      if (setPrototypeImage) {
        setPrototypeImage(imagesJson[0]);
      }
    } else {
      // add the new images to the existing ones
      imagesJson = [...imagesJson, ...resultImages];
    }
    console.log("imagesJson", imagesJson);
  }

  function calculateColumns() {
    thumbColumns = Math.floor(panelWidth / (THUMB_SIZE + 15));
  }

  onMount(() => {
    calculateColumns();
  });

  function handleRowRendered(index) {
    if (index >= imagesJson.length) {
      console.log('LOAD MORE IMAGES?', pagination.current_page, pagination.total_pages);
      if (pagination.current_page < pagination.total_pages) {
        console.log('LOAD MORE IMAGES!');
        loadImages(false);
      }
    }
  }
</script>

<svelte:window on:resize={calculateColumns} />

{#if loading}
  <div in:fade={{ delay:1000, duration: 1000 }}>Loading images...</div>
{:else if imagesJson.length == 0}
  <div>No Images found</div>
{/if}
<div
  bind:clientHeight={panelHeight}
  bind:clientWidth={panelWidth}
  class="wrapper"
  style="--thumbSize: {THUMB_SIZE}px"
>
  <VirtualList
    width="100%"
    height={panelHeight - 5}
    itemCount={Math.ceil(imagesJson.length / thumbColumns)}
    itemSize={THUMB_SIZE + 10}
  >
    <div class="row" slot="item" let:index let:style {style}>
      <ThumbnailRow
        handleRendered={handleRowRendered}
        index={Math.min(imagesJson.length, (index + 1) * thumbColumns)}
        images={imagesJson.slice(index * thumbColumns, (index + 1) * thumbColumns)}
      />
    </div>
  </VirtualList>
</div>


<style>
  .wrapper {
    flex: auto 1 1;
    margin: 0 10px 0 10px;
  }
  .row {
    display: flex;
    flex-direction: row;
    align-items: center;
  }
</style>
