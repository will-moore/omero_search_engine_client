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

#runserver -h 0.0.0.0 -p 5567 --cert=cert.pem --key=key.pem
if __name__ == '__main__':
    manager.run()
