from datetime import datetime, date
from email.mime import image
from DoctorsSchedule import db

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)


class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey(
        'specialization.id'), nullable=False)
    specialization = db.relationship(
        'Specialization', backref=db.backref('specialization', lazy=True))


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(50), nullable=True)
    #start_hour = db.Column(db.String(50), nullable=True)
    #end_hour = db.Column(db.String(50), nullable=True)
    shift = db.Column(db.String(50), nullable=True)
    doctor_name = db.Column(db.String(100), nullable=True)
    doctor_specialization = db.Column(db.String(50), nullable=True)
    logdate = db.Column(db.DateTime, nullable=False, default=datetime.now())


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class Phrases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.Text, nullable=True)
    file_address = db.Column(db.String(100), nullable=True)
    logdate = db.Column(db.DateTime, nullable=False, default=datetime.now())


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# ChangeLog *sequence-based* #major.minor[.build[.revision]] :> versioning


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.Integer, nullable=True)
    minor = db.Column(db.Integer, nullable=True)
    build = db.Column(db.Integer, nullable=True)
    revision = db.Column(db.Integer, nullable=False)
    identifiers = db.Column(db.String(50), nullable=True)  # version
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# create the database and the db table
db.create_all()

# commit the changes
db.session.commit()
