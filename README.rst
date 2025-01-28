Omero search engine client
--------------------------
This web application has a graphic user interface which is used to:

* Build an OMERO query to search metadata (key-value pairs)
* Send the query to the search engine (https://github.com/ome/omero_search_engine)
* Display the results

This is currently a work in progress and is not yet ready for production use.
The app is built using SvelteKit and is a static site; not currently an omoro-web app.

Deploy preview
--------------

The `main` branch is deployed at https://will-moore.github.io/omero_search_engine_client/.

The gh-pages deployment was set-up with help from https://github.com/metonym/sveltekit-gh-pages/tree/master

Development
-----------

```
cd omero_search_engine_client
npm install
npm run dev
```
