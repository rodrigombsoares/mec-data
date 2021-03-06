from mec_data.source.factory import get_source


def download(source_name, year):
    # Get source class
    source = get_source(source_name)
    return source.download(year)
