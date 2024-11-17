<script>
	import { groupStore } from '../groupQueryStore';

	export let keys = [];

	let groups = [];

	groupStore.subscribeGroups((newGroups) => {
		console.log('CentrePanelGroups.svelte -> groups', newGroups);
		groups = newGroups;
	});

	function handleKeyChoice(event) {
		let key = event.target.value;
		groupStore.addGroup(key);
	}
</script>

<select onchange={handleKeyChoice}>
  <option value="">Group by...</option>
	{#each keys as key}
		<option value={key}>{key}</option>
	{/each}
</select>

<div>
	{#each groups as group}
		<span>{group}</span>
	{/each}
</div>

<style>
	span {
		border: solid red 1px;
		padding: 5px;
		margin: 5px;
	}
</style>
