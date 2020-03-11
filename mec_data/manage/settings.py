from dataclasses import dataclass, fields
from envclasses import envclass


@envclass
@dataclass
class DatabaseSettings:
    connstring: str = 'sqlite://'
    
    def prefix(self):
        return 'RETAIL_STORES_DATABASE'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class AthenaSettings:
    access_key: str = ''
    secret_key: str = ''
    region_name: str = 'us-east-1'
    schema_name: str = 'default'
    staging_dir: str = ''
    db: str = 'db_retail_stores_dev'

    def prefix(self):
        return 'RETAIL_STORES_ATHENA'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class DatalakeSettings:
    bucket_name: str = ''
    folder_name: str = ''

    def prefix(self):
        return 'RETAIL_STORES_DATALAKE'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class NeworkSettings:
    host: str = 'localhost'
    port: int = 9000

    def prefix(self):
        return 'RETAIL_STORES_NETWORK'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class IBGEDataSettings:
    url: str = 'http://localhost:9000'

    def prefix(self):
        return 'IBGE_DATA'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class LocationIqSettings:
    max_tries: int = 2
    key: str = ''

    def prefix(self):
        return 'LOCATION_IQ'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class StorageSettings:
    temp_folder: str = ''
    file: str = ''

    def prefix(self):
        return 'RETAIL_STORES_STORAGE'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class DatabricksSettings:
    tenant_url: str = ''
    aws_arn: str = ''
    secret_token: str = ''
    python_script: str = ''

    def prefix(self):
        return 'RETAIL_STORES_DATABRICKS'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class GeneralSettings:
    report_client: str = 'azure'
    process_client: str = ''
    datalake_query_client: str = ''
    geocoding_client: str = ''

    def prefix(self):
        return 'RETAIL_STORES'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class ParquetAppSettings:
    rawdata_folder: str = ''
    parquets_folder: str = ''
    jar_path: str = ''
    database: str = ''

    def prefix(self):
        return 'RETAIL_STORES_PARQUETAPP'

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + '_' + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class AzureSettings:
    active_directory_tenant_id: str = 'd269b743-c6ab-4485-85ee-c7f60d0b261b/'
    active_directory_base_authority: str = 'https://login.microsoftonline.com/'
    group_id: str = 'aa9ed7a0-61a2-4583-81e2-f13e10d1981c'
    retail_stores_dataset_id: str = '310964aa-2ed3-49f9-8495-5b83d745fb91'
    app_id: str = '96ae2af8-9b0e-4ee4-9de1-dabedf2076ab'
    app_secret: str = 'sSqDtAmAYPvInQxc/+9qjLI6q/arvPAqrXJSA47UsKQ='
    pbi_resource: str = 'https://analysis.windows.net/powerbi/api'

    def prefix(self):
        return "AZURE"

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + "_" + setting.name.upper()] = getattr(
                self, setting.name
            )
