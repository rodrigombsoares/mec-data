from dataclasses import dataclass, fields
from envclasses import envclass


@envclass
@dataclass
class DatabaseSettings:
    connstring: str = "sqlite:///app.db"

    def prefix(self):
        return "MEC_DATA_DATABASE"

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + "_" + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class DatalakeSettings:
    bucket_name: str = ""
    folder_name: str = ""
    client: str = "local"

    def prefix(self):
        return "MEC_DATA_DATALAKE"

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + "_" + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class NeworkSettings:
    host: str = "localhost"
    port: int = 9000

    def prefix(self):
        return "MEC_DATA_NETWORK"

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + "_" + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class DataSourceSettings:
    url: str = "http://localhost:9000"
    scholar_census: str = ""
    university_census: str = ""

    def prefix(self):
        return "DATA_SOURCE"

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + "_" + setting.name.upper()] = getattr(
                self, setting.name
            )


@envclass
@dataclass
class StorageSettings:
    temp_folder: str = ""
    file: str = ""

    def prefix(self):
        return "MEC_DATA_STORAGE"

    def configure(self, app) -> None:
        for setting in fields(self):
            app.config[self.prefix() + "_" + setting.name.upper()] = getattr(
                self, setting.name
            )
