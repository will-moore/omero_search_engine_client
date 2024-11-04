import { writable, get } from 'svelte/store';

export class SearchQueryStore {
	constructor() {
		this.and_filters = writable([]);
	}

    addFilter({key, value, dtype, operator = 'equals', resource = 'image'}) {
        console.log("addFilter", key, value, dtype, operator, resource);
        this.and_filters.update(filters => [...filters, {key, value, operator, resource}]);
    }

    getAndFilters() {
        return get(this.and_filters);
    }

    getQuery() {
        return {
            resource: 'image',
            query_details: {
                and_filters: get(this.and_filters),
                or_filters: [],
                case_sensitive: false
            },
            mode: 'searchterms'
        }
    }

    subscribeAndFilters(run) {
        return this.and_filters.subscribe(run);
    }
}

export const queryStore = new SearchQueryStore();

// let d = {
// 	resource: 'image',
// 	query_details: {
// 		and_filters: [{ name: 'Gene Symbol', value: 'ints11', operator: 'equals', resource: 'image' }],
// 		or_filters: [],
// 		case_sensitive: false
// 	},
// 	mode: 'searchterms'
// };
