from flask import Flask
from flask_bootstrap import Bootstrap
import sys
from logging.handlers import RotatingFileHandler
import logging
import os
from omero_search_client.configuration.config import omero_search_client_app_config, load_configuration_variables_from_file,configLooader
omero_client_app = Flask(__name__)


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
    return omero_client_app

