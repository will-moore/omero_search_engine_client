import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// See https://svelte.dev/docs/kit/adapters for more information about adapters.

		// For static sites, use the `adapter-static` adapter
		// https://svelte.dev/docs/kit/adapter-static#Options
		adapter: adapter(),
		paths: {
		    base: process.env.NODE_ENV === "production" ? "/omero_search_engine_client" : "",
		},
	}
};

export default config;
