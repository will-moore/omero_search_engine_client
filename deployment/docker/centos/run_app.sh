#!/bin/bash
echo "$@"
#test if the configuration file exists, if not it will copy it from the app configuration folder
test -f /etc/searchengineclient/.omero_search_client.yml || cp /searchengineclient/omero_search_client/configuration/omero_search_client.yml /etc/searchengineclient/.omero_search_client.yml

#Check inequality of a variable with a string value

if [ -z  "$@" ] || [ "$@" = "run_app" ]; then
  echo "Windows operating system"
  bash start_gunicorn_serch_engine_client.sh
else
  python3.9 manage.py "$@"
fi

