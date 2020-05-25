from mec_data.model.databases import data_warehouse as db


class ScholarStudent(db.Model):

    __tablename__ = "scholar_student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    day_birth = db.Column(db.Integer)
    month_birth = db.Column(db.Integer)
    year_birth = db.Column(db.Integer)
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    race = db.Column(db.Integer)
    nationality = db.Column(db.Integer)
    uf_birth = db.Column(db.Integer)
    city_birth = db.Column(db.Integer)
    disability = db.Column(db.Integer)

    public_transp = db.Column(db.Integer)
    school_uf = db.Column(db.Integer)
    school_dependency = db.Column(db.Integer)
    school_location = db.Column(db.Integer)

    class_type = db.Column(db.Integer)
    class_duration = db.Column(db.Integer)
    class_days = db.Column(db.Integer)
