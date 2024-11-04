
<script>
    import { queryStore } from './searchQueryStore.js';

    export let result;
    console.log('AutocompleteItem', result);

    function handleClick() {
        console.log('Adding filter', result);
        queryStore.addFilter(result);
    }
</script>


<li> <button on:click={handleClick}> {@html result.label} </button></li>

