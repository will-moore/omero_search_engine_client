


<script>
	export let items;
	export let handleClick;
</script>

<ul class="items">
	{#each items as item (item)}
		<li>
			<label>
				<button on:click={() => handleClick(item)}>
					{item.dtype == "container" ? "Container" : ""}
					<strong>{item.key}:</strong>
					{item.value}
					<span style="opacity: 0.3">({item.count})</span>
					({item.data_source})
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
		color: inherit;
	}
</style>
