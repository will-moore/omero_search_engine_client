
import { BASE_URL } from "./searchengine";

export async function getJson(url, options = {}) {
    const response = await fetch(url, options);
    return await response.json();
}

export function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

export async function loadHierarchy(child) {
    let url = `${BASE_URL}webclient/api/paths_to_object/?${child.type}=${child.id}`;
    let hierarchy = await getJson(url);
    return hierarchy.paths;
}
