"""
Main Flask app definition
"""
import logging
import os

import dotenv

from envclasses import load_env
from flask import Flask, Blueprint, url_for, jsonify, render_template

# # Import configuration
from mec_data.manage.settings import (
    DatabaseSettings,
    DatalakeSettings,
    NeworkSettings,
    DataSourceSettings,
    StorageSettings,
)

# Import database
from mec_data.model.databases import data_warehouse


def register_routes(api):
    from mec_data.controller.data_source import api as data_source_api
    from mec_data.controller.data_lake import api as data_lake_api
    from mec_data.controller.data_warehouse import api as data_warehouse

    api.add_namespace(data_source_api, path=f"/download")
    api.add_namespace(data_lake_api, path=f"/store")
    api.add_namespace(data_warehouse, path=f"/data_warehouse")


def configure_app(app):
    # Load .env file
    dotenv.load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

    # Database configuration
    db_settings = DatabaseSettings()
    load_env(db_settings, prefix=db_settings.prefix())
    db_settings.configure(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["MEC_DATA_DATABASE_CONNSTRING"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # silence deprecation warning

    # Datalake configuration
    data_lake_settings = DatalakeSettings()
    load_env(data_lake_settings, prefix=data_lake_settings.prefix())
    data_lake_settings.configure(app)

    # Network configuration
    network_settings = NeworkSettings()
    load_env(network_settings, prefix=network_settings.prefix())
    network_settings.configure(app)

    # Datasource configuration
    data_source_settings = DataSourceSettings()
    load_env(data_source_settings, prefix=data_source_settings.prefix())
    data_source_settings.configure(app)

    # Storage configuration
    storage_settings = StorageSettings()
    load_env(storage_settings, prefix=storage_settings.prefix())
    storage_settings.configure(app)

    # # General configuration
    # general_settings = GeneralSettings()
    # load_env(general_settings, prefix=general_settings.prefix())
    # general_settings.configure(app)
    return app


def configure_restplus(app_name):
    """
        Override flask_restplus apidoc variable passing the apps
        name as a paramenter but still pointing to the library's
        folders /template and /static

        Now swagger calls statics at /{app_name}/swaggerui/{static_file}
    """
    from flask_restplus import apidoc

    apidoc.apidoc = apidoc.Apidoc(
        "restplus_doc",
        __name__,
        template_folder=os.path.dirname(apidoc.__file__) + "/templates",
        static_folder=os.path.dirname(apidoc.__file__) + "/static",
        static_url_path=f"/{app_name}/swaggerui",
    )
    # redefine swagger_static
    @apidoc.apidoc.add_app_template_global
    def swagger_static(filename):
        return url_for("restplus_doc.static", filename=filename)


def create_app():
    from flask_restplus import Api

    app_name = "mec-data"
    # Set flask restplus to work with our app name
    configure_restplus(app_name)
    # Create flask app
    app = Flask(__name__)
    # Create a blueprint for the api setting our app's name as url prefix
    blueprint = Blueprint("api", __name__, url_prefix=f"/{app_name}")
    # Create an Api from that blueprint
    api = Api(blueprint)
    # Register blueprint and continue configuration
    app.register_blueprint(blueprint)
    app.logger.setLevel(logging.ERROR)
    app = configure_app(app)
    register_routes(api)

    # Initialise databases
    data_warehouse.init_app(app)
    with app.app_context():
        data_warehouse.create_all()

    return app
