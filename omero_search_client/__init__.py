from flask import Flask
from flask_bootstrap import Bootstrap
from logging.handlers import RotatingFileHandler
import logging
import os
from urllib.parse import urlparse
from flask import request, url_for as _url_for

from omero_search_client.configuration.config import omero_search_client_app_config, load_configuration_variables_from_file,configLooader
main_folder=os.path.dirname(os.path.realpath(__file__))

static_folder=os.path.join(main_folder, "searchengineclientstatic")
omero_client_app = Flask(__name__, static_url_path="/searchengineclientstatic", static_folder="searchengineclientstatic")

'''
Refernce for the following two methods is:
https://stackoverflow.com/questions/25962224/running-a-flask-application-at-a-url-that-is-not-the-domain-root
'''
def url_with_host(path):
    return '/'.join((urlparse(request.host_url).path.rstrip('/'), path.lstrip('/')))

def url_for(*args, **kwargs):
    if kwargs.get('_external') is True:
        return _url_for(*args, **kwargs)
    else:
        return url_with_host(_url_for(*args, **kwargs))

def create_app(config_name="development"):
    app_config=configLooader.get(config_name)
    load_configuration_variables_from_file((app_config))
    omero_client_app.config.from_object(app_config)
    bootstrap = Bootstrap(omero_client_app)

    omero_client_app.app_context().push()
    log_folder = os.path.join(os.path.expanduser('~'), 'logs')
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    file_handler = RotatingFileHandler(os.path.join(log_folder, 'omero_search_engine_client.log'), maxBytes=100240,
                                           backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    omero_client_app.logger.addHandler(file_handler)
    omero_client_app.logger.setLevel(logging.INFO)
    omero_client_app.logger.info('App  startup')
    from omero_search_client.main import main as routers_blueprint_main
    omero_client_app.register_blueprint(routers_blueprint_main, url_prefix='/')
    omero_client_app.jinja_env.globals['url_for'] = url_for
    if config_name!= "testing":
        from omero_search_client.app_data import check_copy_data_file
        check_copy_data_file(omero_client_app)
    return omero_client_app

'''
commented as it is ebaled at the NGINX confiuration level
#add it to account for CORS
@omero_client_app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header["Access-Control-Allow-Headers"]= "*"
    return response

'''