from mec_data.source.factory import get_source
from mec_data.data_lake import get_dl_client


def load(source_name, year):
    source = get_source(source_name)
    dl_client = get_dl_client()
    # Get csv
    csv_files = dl_client.get_files(source.bucket, f"{source.bucket}_{year}")
    # Read csv according to source and load to DW
    for csv_file in csv_files:
        source.load_to_dw(csv_file)
    return "load"
