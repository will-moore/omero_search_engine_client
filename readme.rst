Omero search engine client
--------------------------
This web application has a graphic user interface which is used to:

* build an OMERO query to search metadata (key-value pairs)
* send the query to the search engine (https://github.com/ome/omero_search_engine)
* display the results when the they are ready.
* export the results to csv file (default file name is export.csv).

Install
=======

This is an OMERO.web app that should be installed in the same environment as `omero-web`.

Install (dev) and add to `omero-web` apps:

      $ pip install -e .
      $ omero config append omero.web.apps '"omero_search_engine_client"'

The autocomplete function for the atribute value fields gets their suggested values from the search engine.
As has been mentioned above, the app performs quries by sending them to the query search engine.
So, the search engine should run and configured before running:

The following command will configure the url for the search engine:

     $ omero config set omero.web.searchengine.url "https://SERVER/searchengineapi/api/v1"

If the search engine is run locally, its url should be something like: "http://127.0.0.1:5577/"

After restarting `omero-web`, go to [omero-web-server]/searchengine/

It is possible to deploy the app and the searchengine using Docker images. For more information, please use the following link:
https://github.com/ome/omero_search_engine/blob/main/docs/configuration/configuration_installtion.rst

