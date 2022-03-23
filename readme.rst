Omero search engine client
--------------------------
This web application has a graphic user interface which is used to:

* build an omero query to search metadata (key-value pairs)
* send the query to the search engine (https://github.com/ome/omero_search_engine)
* display the results when the they are ready.
* export the results to csv file (default file name is export.csv).

The autocomplete function for the atribute value fields gets their suggested values from the search engine.
As has beeb mentioned above, the app perform quries by sending them to the query search engine.
So, the search engine should run and configured before running

The following command will configure the url for the search engine:

.. code-block::

     path/to/python manage.py set_searchengine_url -u "serahc engine url"

If the serahc engine run locally, its url should be something like that: "http://127.0.0.1:5577/"

Also, it is needed to setup app data folder using the following command:

.. code-block::

      path/to/python manage.py set_app_data_folder -a path/to/data/folder

It is possible to deploy the app and the searchengine using Docker images. For more information, please use the following link:
https://github.com/ome/omero_search_engine/blob/main/docs/configuration/configuration_installtion.rst

