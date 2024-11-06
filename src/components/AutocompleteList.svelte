


<script>
	// import { send, receive } from './transition.js';

	// import {queryStore} from '../searchQueryStore.js';

	// let { items, handleClick, filterIndex } = $props();

	export let items;
	export let handleClick;

	// function handleOperatorChange(event) {
	// 	console.log('Operator change', event.target.value);
	// }
</script>

Length: {items.length}
<ul class="items">
	{#each items as item (item)}
		<li>
			<label>
				<!-- <input type="checkbox" bind:checked={item.picked}/> -->
				<button on:click={() => handleClick(item)}>
					<strong>{item.key}:</strong>
					{item.value}
				</button>
			</label>
		</li>
	{/each}
</ul>

<style>
	label {
		width: 100%;
		height: 100%;
		display: flex;
	}

	ul {
		list-style-type: none;
		padding: 0;
	}
	li {
		list-style: none;
	}
	li:hover {
		background-color: blue;
		color: white;
	}

	button {
		border: none;
		background-color: transparent;
		word-wrap: break-word;
		cursor: pointer;
		text-align: left;
	}
</style>
