from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields, validate
from .models import MyTable
from .extensions import db

class MyTableSchema(SQLAlchemySchema):
    class Meta:
        model = MyTable
        load_instance = True
        sqla_session = db.session

    id = auto_field(dump_only=True)
    first_name = auto_field(required=True, validate=validate.Length(min=2, max=100))
    last_name = auto_field(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = auto_field()
    birth_date = fields.Date(required=True)
    city_id = auto_field(required=True)
    salary_grade_id = auto_field(required=True)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)