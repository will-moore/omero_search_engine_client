<script>
	import { queryStore } from '../searchQueryStore.js';

	let filters = [];

	let query = {};

	queryStore.subscribeFilters((newFilters) => {
		filters = newFilters;
		query = queryStore.getQuery();
	});
</script>

<code
	><pre>
{JSON.stringify(query, null, 2)}
</pre></code
>
