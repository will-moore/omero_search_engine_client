Omero search engine client
--------------------------
This web application has a graphic user interface which is used to:

* build an OMERO query to search metadata (key-value pairs)
* send the query to the search engine (https://github.com/ome/omero_search_engine)
* display the results when the they are ready.
* export the results to csv file (default file name is export.csv).

This is currently a work in progress and is not yet ready for production use.
The app is built using SvelteKit and is a static site; not currently an omoro-web app.

Deploy preview
--------------

You can access a static build of the app at https://omero-search-engine-client.netlify.app/


Development
-----------

```
cd omero_search_engine_client
npm install
npm run dev
```
