from mec_data.model.university import UniversityStudent
from mec_data.model.databases import data_warehouse


def create_many(students):
    data_warehouse.session.bulk_save_objects(students)
    data_warehouse.session.commit()
