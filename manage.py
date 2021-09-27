from omero_search_client import omero_client_app, create_app
from flask_script import Manager
omero_client_app=create_app()
manager = Manager(omero_client_app)

'''
Script to run the application in th development mode
It is also can be used to application script command
'''
#runserver -h 0.0.0.0 -p 5567 --cert=cert.pem --key=key.pem
if __name__ == '__main__':
    manager.run()
