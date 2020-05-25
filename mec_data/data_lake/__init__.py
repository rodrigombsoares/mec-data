from flask import current_app


def get_dl_client():
    client_name = current_app.config.get("MEC_DATA_DATALAKE_CLIENT")
    if client_name == "local":
        from mec_data.data_lake.local import LocalDL

        return LocalDL()
