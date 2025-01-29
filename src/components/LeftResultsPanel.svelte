<script>
  import { queryStore } from '../searchQueryStore.js';
  import { selectedContainerStore, containerStore } from '../containerStore.js';

  import folder16png from '../lib/assets/folder16.png';
  import folderScreen16png from '../lib/assets/folder_screen16.png';

  let resultContainers = [];
  let selectedContainer = null;

  containerStore.subscribe((containers) => {
    resultContainers = containers;
  });

  queryStore.subscribeFilters((newFilters) => {
    // This is called when filters change AND when we initially subscribe
    let query = queryStore.getQuery();
    console.log('SEARCHING....', query);
    containerStore.loadContainers(query);
  });
  // When the selected container changes (e.g. click below OR history back/foward)
  // we need to update the filters
  selectedContainerStore.subscribe((container) => {
    selectedContainer = container;
  });

  function handleClick(container) {
    console.log('Clicked', container);
    selectedContainerStore.set(container);
  }
</script>

<div class="scrollable">
  {#if resultContainers.length == 0}
    <!-- Spinner appears in middle of page since position is absolute -->
    <div class="spinner"></div>
    <p>Loading containers...</p>
  {/if}
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
            {#if container.data_source}
              <span>({container.data_source})</span>
            {/if}
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

  @keyframes spinner {
    to {
        transform: rotate(360deg);
    }
}

  .spinner:after {
    content: "";
    box-sizing: border-box;
    position: absolute;
    top: 50%;
    left: 50%;
    width: 50px;
    height: 50px;
    margin-top: -20px;
    margin-left: -20px;
    border-radius: 50%;
    border: 5px solid rgba(180, 180, 180, 0.6);
    border-top-color: rgba(0, 0, 0, 0.6);
    animation: spinner 0.6s linear infinite;
  }
</style>
