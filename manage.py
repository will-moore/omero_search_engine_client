from omero_search_client import omero_client_app, create_app
from flask_script import Manager
omero_client_app=create_app()
manager = Manager(omero_client_app)
from omero_search_client.configuration.config import update_config_file

'''
Script to run the application in th development mode
It is also can be used to application script command
'''

@manager.command
@manager.option('-u', '--url', help='Search engine url')
def set_searchengine_url (url=None):
    if url:
        update_config_file({"OMERO_SEARCH_ENGINE_BASE_URL":url})
    else:
        omero_client_app.logger.info("No attribute is provided")

@manager.command
@manager.option('-d', '--url', help='app data folder')
def set_app_data_folder (app_data=None):
    if app_data:
        update_config_file({"APP_DATA_FOLDER":app_data})
    else:
        omero_client_app.logger.info("No attribute is provided")

@manager.command
@manager.option('-s', '--secret_key', help='cache folder path')
def set_client_secret_key (secret_key=None):
    if secret_key:
        update_config_file({"SECRET_KEY":secret_key})
    else:
        omero_client_app.logger.info("No value is provided")

#runserver -h 0.0.0.0 -p 5567 --cert=cert.pem --key=key.pem
if __name__ == '__main__':
    manager.run()
