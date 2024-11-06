import { writable, get } from 'svelte/store';

export class SearchQueryStore {
    // We store the filters in a 2D array of filters, so the query looks like:
    // [[Filter 1a, OR Filter 1b], AND [Filter 2], AND [Filter 3a, OR Filter 3b]]
    // When we build the query, if there is only a single filter [Filter 2], it becomes an `and_filter`
    // and the others are `or_filters`.
	constructor() {
		this.filters = writable([]);
        // set to the index of the filter being edited - used to trigger FilterPopover
        this.filterBeingEdited = writable(-1);
	}

    // Add a new AND filter (list) to the store
    addFilter({key, value, dtype, operator = 'equals', resource = 'image'}) {
        // NB: api uses 'name' instead of 'key' https://github.com/ome/omero_search_engine/issues/42
        let newFilter = {name:key, value, dtype, operator, resource, active: true};
        let editedFilter = this.getFilterBeingEdited();
        console.log("STORE addFilter: editedFilter", editedFilter, newFilter);
        if (editedFilter == -1) {
            let newOrFilters = [newFilter];
            this.filters.update(filters => [...filters, newOrFilters]);
            // return the index of the new filter (last in the list)
            editedFilter = get(this.filters).length - 1;
            this.editFilter(editedFilter);
        } else {
            this.filters.update((filters) => {
                // add the newFilter to the OR filters at the given index
                return filters.map((f, index) => index == editedFilter ? [...f, newFilter] : f);
            });
        }
        return editedFilter;
    }

    getFilters() {
        return get(this.filters);
    }

    getQuery(containerName) {
        // ignore filters that are not active:
        // TODO: recursively filter individual filters instead of whole or_filter list;
        let filters = get(this.filters).filter(f => f[0].active);
        let or_filters = filters.filter(f => f.length > 1);
        let and_filters = filters.filter(f => f.length === 1).map(f => f[0]);
        if (containerName) {
            // {name: "name", value: "idr0012-fuchs-cellmorph/screenA", operator: "equals", resource: "container"}
            and_filters.push({name: "name", value: containerName, operator: "equals", resource: "container"});
        }
        return {
            resource: 'image',
            query_details: {
                and_filters,
                or_filters,
                case_sensitive: false
            },
            mode: 'searchterms'
        }
    }

    toggleFilter(index) {
        this.filters.update(filters => {
            let newFilters = [...filters];
            newFilters[index] = newFilters[index].map(f => {
                f.active = !f.active;
                return f;
            });
            return newFilters;
        });
    }

    removeFilter(index) {
        this.filters.update(filters => filters.filter((f, i) => i !== index));
    }

    editFilter(index) {
        // triggers a modal to edit the filter
        this.filterBeingEdited.set(index);
    }
    getFilterBeingEdited() {
        return get(this.filterBeingEdited);
    }

    subscribeFilters(run) {
        return this.filters.subscribe(run);
    }
    subscribeFilterBeingEdited(run) {
        return this.filterBeingEdited.subscribe(run);
    }
}

// Single instance of the query store
export const queryStore = new SearchQueryStore();

// Selected container. E.g. {id: 123, type: "screen", name: "idr0012-fuchs-cellmorph/screenA"}
export const selectedContainerStore = writable(null);

// Selected image. E.g. {id: 123, name: "image.tiff"}
export const selectedImageStore = writable(null);

// let d = {
// 	resource: 'image',
// 	query_details: {
// 		or_filters: [{ name: 'Gene Symbol', value: 'ints11', operator: 'equals', resource: 'image' }],
// 		or_filters: [],
// 		case_sensitive: false
// 	},
// 	mode: 'searchterms'
// };
