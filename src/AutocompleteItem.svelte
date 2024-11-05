
<script>
    // import { queryStore } from './searchQueryStore.js';

    export let result;
    export let handleClick
    console.log('AutocompleteItem', result);

    // function handleClick() {
    //     console.log('Adding filter', result);
    //     queryStore.addFilter(result);
    // }
</script>


<li> <button on:click={() => handleClick(result)}> {@html result.label} </button></li>

