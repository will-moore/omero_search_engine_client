import os
from shutil import copyfile

def check_copy_data_file(omero_client_app):
    '''
    copy the json file which contains the search term to the app_data folder if it does not exist
    Args:
        omero_client_app:
    Returns:
    '''
    if omero_client_app.config.get("APP_DATA_FOLDER") == "/path/to/app/data/folder":
        return
    search_terms=os.path.join(omero_client_app.config.get("APP_DATA_FOLDER"), "restricted_search_terms.json")

    if not os.path.isfile(search_terms):
        LOCAL_DATA_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                       'restricted_search_terms.json')
        if os.path.isdir(os.path.join(omero_client_app.config.get("APP_DATA_FOLDER"))):
            copyfile(LOCAL_DATA_FILE, search_terms)