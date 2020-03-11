"""
Main Flask app definition
"""
import logging
import os

import dotenv

from envclasses import load_env
from flask import (
    Flask, 
    Blueprint, 
    url_for, 
    jsonify, 
    render_template
)

# # Import configuration
from retail_stores.manage.settings import (
    NeworkSettings,
    DatabaseSettings,
    DatalakeSettings,
    IBGEDataSettings,
    ParquetAppSettings,
    GeneralSettings,
    DatabricksSettings,
    AthenaSettings,
    LocationIqSettings,
    StorageSettings,
    AzureSettings
#     DatasourceSettings,
)

# Import database
from retail_stores.model.databases import data_warehouse


def register_routes(api):
    from retail_stores.controller.company import api as company_api
    from retail_stores.controller.crawl import api as crawl_api
    from retail_stores.controller.ibge_data import api as ibge_data_api
    from retail_stores.controller.cluster import api as cluster_api
    from retail_stores.controller.process import api as process_api
    from retail_stores.controller.data_warehouse import api as data_warehouse
    from retail_stores.controller.report import api as report

    api.add_namespace(company_api, path=f'/company')
    api.add_namespace(crawl_api, path=f'/crawl')
    api.add_namespace(ibge_data_api, path=f'/ibge_data')
    api.add_namespace(cluster_api, path=f'/cluster')
    api.add_namespace(process_api, path=f'/process')
    api.add_namespace(data_warehouse, path=f'/data_warehouse')
    api.add_namespace(report, path=f'/report')


def configure_app(app):
    # Load .env file
    dotenv.load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

    # Network configuration
    network_settings = NeworkSettings()
    load_env(network_settings, prefix=network_settings.prefix())
    network_settings.configure(app)

    # Database configuration
    db_settings = DatabaseSettings()
    load_env(db_settings, prefix=db_settings.prefix())
    db_settings.configure(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['RETAIL_STORES_DATABASE_CONNSTRING']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence deprecation warning

    # # Datasource configuration
    # data_source_settings = DatasourceSettings()
    # load_env(data_source_settings, prefix=data_source_settings.prefix())
    # data_source_settings.configure(app)

    # Ibge data configuration
    ibge_data_settings = IBGEDataSettings()
    load_env(ibge_data_settings, prefix=ibge_data_settings.prefix())
    ibge_data_settings.configure(app)

    # Datalake configuration
    data_lake_settings = DatalakeSettings()
    load_env(data_lake_settings, prefix=data_lake_settings.prefix())
    data_lake_settings.configure(app)

    # Storage configuration
    storage_settings = StorageSettings()
    load_env(storage_settings, prefix=storage_settings.prefix())
    storage_settings.configure(app)

    # Databricks configuration
    databricks_settings = DatabricksSettings()
    load_env(databricks_settings, prefix=databricks_settings.prefix())
    databricks_settings.configure(app)

    # ParquetApp configuration
    parquetApp_settings = ParquetAppSettings()
    load_env(parquetApp_settings, prefix=parquetApp_settings.prefix())
    parquetApp_settings.configure(app)

    # General configuration
    general_settings = GeneralSettings()
    load_env(general_settings, prefix=general_settings.prefix())
    general_settings.configure(app)

    # Athena configuration
    athena_settings = AthenaSettings()
    load_env(athena_settings, prefix=athena_settings.prefix())
    athena_settings.configure(app)

    # LocationIQ configuration
    location_iq_settings = LocationIqSettings()
    load_env(location_iq_settings, prefix=location_iq_settings.prefix())
    location_iq_settings.configure(app)

    # LocationIQ configuration
    azure_settings = AzureSettings()
    load_env(azure_settings, prefix=azure_settings.prefix())
    azure_settings.configure(app)
    return app


def configure_restplus(app_name):
    """
        Override flask_restplus apidoc variable passing the apps 
        name as a paramenter but still pointing to the library's 
        folders /template and /static

        Now swagger calls statics at /{app_name}/swaggerui/{static_file}
    """
    from flask_restplus import apidoc
    apidoc.apidoc = apidoc.Apidoc('restplus_doc', __name__,
        template_folder=os.path.dirname(apidoc.__file__) + '/templates',
        static_folder=os.path.dirname(apidoc.__file__) + '/static',
        static_url_path=f'/{app_name}/swaggerui'
    )
    # redefine swagger_static
    @apidoc.apidoc.add_app_template_global
    def swagger_static(filename):
        return url_for('restplus_doc.static', filename=filename)


def create_app():
    from flask_restplus import Api
    app_name = 'retail-stores'
    # Set flask restplus to work with our app name
    configure_restplus(app_name)
    # Create flask app
    app = Flask(__name__)
    # Create a blueprint for the api setting our app's name as url prefix
    blueprint = Blueprint('api', __name__, url_prefix=f'/{app_name}')
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
