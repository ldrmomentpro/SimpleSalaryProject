from datetime import datetime, timezone
from .extensions import db

class MyTable(db.Model):
    __tablename__ = 'mytable'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    salary_grade_id = db.Column(db.Integer, db.ForeignKey('salary_grade.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cities = db.relationship('City', backref='country', lazy=True)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    users = db.relationship('MyTable', backref='city', lazy=True)

class SalaryGrade(db.Model):
    __tablename__ = 'salary_grade'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer, unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    users = db.relationship('MyTable', backref='salary_grade', lazy=True)
