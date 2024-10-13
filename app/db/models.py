from app.db.database import db

# Clase base para todos los modelos
class BaseModel(db.Model):
    """ Clase base para todos los modelos """
    __abstract__ = True

class Employee(BaseModel):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    department_id = db.Column(db.Integer)
    job_id = db.Column(db.Integer)

class Department(BaseModel):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String)

class Job(BaseModel):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String)
