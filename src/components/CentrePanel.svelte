<script>
	import { groupStore } from '../groupQueryStore';
	import { queryStore } from '../searchQueryStore.js';
	import CentrePanelGroups from './CentrePanelGroups.svelte';
	import Groups from './Groups.svelte';
	import Images from './Images.svelte';

	const THUMB_SIZE = 64;

	// Group images by these keys
	/**
	 * @type {string | any[]}
	 */
	let groups = [];
	$: queryWithoutContainer = queryStore.getQuery();

  /**
   * When images are loaded in <Images>, this gets populated for the <CentrePanelGroups> component
   * @type {string[]}
   */
	$: imageKeys = [];

	function setPrototypeImage(prototypeImage) {
		if (prototypeImage) {
			imageKeys = prototypeImage.key_values.map((/** @type {{ name: any; }} */ kv) => kv.name);
		} else {
			imageKeys = [];
		}
	}

	// if the filters changes, we need to update the query we pass down to the groups
	queryStore.subscribeFilters(() => {
		// Since we add the container name to /container_filterkeyvalues/ URL we don't need to
		// include any filters that are container specific. So we exclude them...
		// https://github.com/ome/omero_search_engine/pull/102#issuecomment-2611377390
		let ingoreContainerFilters = true;
		queryWithoutContainer = queryStore.getQuery(null, ingoreContainerFilters);
	});

	groupStore.subscribeGroups((/** @type {any[]} */ newGroups) => {
		groups = newGroups;
	});
</script>

<div class="header">
	<CentrePanelGroups keys={imageKeys} />
</div>

{#if groups.length > 0}
	<!-- Force re-render if first group changes.
    Groups are cleared in CentrePanelGroups when selected container or query changes -->
	{#key groups[0]}
		<div class="wrapper" style="--thumbSize: {THUMB_SIZE}px">
			<Groups parentQuery={queryWithoutContainer} key={groups[0]} />
		</div>
	{/key}
{:else}
	<Images {setPrototypeImage} />
{/if}

<style>
	.header {
		flex: 0 0 auto;
		background-color: #f1f0f4;
		border-bottom: solid #ddd 1px;
	}
	.wrapper {
		/* 300px to force scrollbar */
		height: 300px;
		flex: auto 1 1;
		margin: 0 10px 0 10px;
		overflow: auto;
	}
</style>
