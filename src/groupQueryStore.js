import { writable, get } from 'svelte/store';

export class GroupQueryStore {
    // We "group" images within a Study by their KVP Keys. 
	constructor() {
		this.groups = writable([]);
        
        // this.containerName = writable("");
	}

    addGroup(key) {
        this.groups.update(groups => [...groups, key]);
    }

    removeGroup(index) {
        this.groups.update(groups => {
            groups.splice(index, 1);
            return groups;
        });
    }

    subscribeGroups(run) {
        return this.groups.subscribe(run);
    }

    setGroups(groups) {
        this.groups.set(groups);
    }
}

// Single instance of the group store
export const groupStore = new GroupQueryStore();
