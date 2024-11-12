<script>
  import { get } from 'svelte/store';
  import VirtualList from 'svelte-tiny-virtual-list';

  import { queryStore, selectedContainerStore } from '../searchQueryStore.js';
  import { submitSearch } from '../searchengine.js';
  import ThumbnailRow from './ThumbnailRow.svelte';
  import { onMount } from 'svelte';

  const THUMB_SIZE = 64;
  let panelHeight = 0;
  let panelWidth = 0;

  let imagesJson = [];

  // re-calculated based on panelWidth
  $: thumbColumns = 7;

  let pagination = null;
  let controller;

  // if either the filters or the selected container changes, we need to reload the images
  queryStore.subscribeFilters((newFilters) => {
    loadImages();
  });
  selectedContainerStore.subscribe((obj_id) => {
    loadImages();
  });

  async function loadImages(clear = true) {
    console.log('loadImages... clear', clear);
    let obj = get(selectedContainerStore);
    if (!obj?.name) {
      imagesJson = [];
      pagination = null;
      return;
    }
    let query = queryStore.getQuery(obj.name);
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
    controller = new AbortController();
    let data = await submitSearch(query, false, { signal: controller.signal });

    console.log('LOADIMAGES -> data images', data.results.results.length, data);
    // Store pagination info...
    // total_pages = data.results.total_pages;
    pagination = data.results.pagination;

    if (clear) {
      // replace the existing images
      imagesJson = data.results.results;
    } else {
      // add the new images to the existing ones
      imagesJson = [...imagesJson, ...data.results.results];
    }
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

<div class="header">
  <!-- {imagesJson.length} / {thumbColumns} - height {panelHeight} -->
</div>

<div
  bind:clientHeight={panelHeight}
  bind:clientWidth={panelWidth}
  class="wrapper"
  style="--thumbSize: {THUMB_SIZE}px"
>
  <VirtualList
    width="100%"
    height={panelHeight - 15}
    itemCount={Math.ceil(imagesJson.length / thumbColumns)}
    itemSize={THUMB_SIZE + 10}
  >
    <div class="row" slot="item" let:index let:style {style}>
      <ThumbnailRow
        handleRendered={handleRowRendered}
        index={(index + 1) * thumbColumns}
        images={imagesJson.slice(index * thumbColumns, (index + 1) * thumbColumns)}
      />
    </div>
  </VirtualList>
</div>

<style>
  .header {
    flex: 0 0 40px;
    background-color: #f1f0f4;
    border-bottom: solid #ddd 1px;
  }
  .wrapper {
    flex: auto 1 1;
    /* height: 100%; */
    margin: 0 10px 0 10px;
  }
  .row {
    text-align: center;
  }
</style>
