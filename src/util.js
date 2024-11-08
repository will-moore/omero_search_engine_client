
import { BASE_URL } from "./searchengine";

export async function getJson(url) {
    const response = await fetch(url);
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
