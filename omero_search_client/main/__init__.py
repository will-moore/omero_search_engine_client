from flask import Blueprint
main= Blueprint('main', __name__)
import omero_search_client.main.views
