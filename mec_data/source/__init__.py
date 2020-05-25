def get_source(source_name):
    """
    A simple factory for getting source class
    """
    if source_name == "SCHOLAR_CENSUS":
        from mec_data.source.scholar import ScholarSource

        return ScholarSource()
    elif source_name == "UNIVERSITY_CENSUS":
        from mec_data.source.university import UniversitySource

        return UniversitySource()
