from .models import MyTable
from .schemas import MyTableSchema
from .extensions import db
from marshmallow import ValidationError

schema = MyTableSchema()

def add(record):
    try:
        data = schema.load(record)
        db.session.add(data)
        db.session.commit()
        return data, None
    except ValidationError as err:
        return None, err.messages

def delete(id):
    record = MyTable.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return record, None

def edit(id, data):
    record = MyTable.query.get_or_404(id)
    try:
        edited_data = schema.load(data, partial=True)
        for key, value in edited_data.__dict__.items():
            if key != "_sa_instance_state":
                setattr(record, key, value)
        db.session.commit()
        return record, None
    except ValidationError as e:
        return None, e.messages

def list_records():
    records = MyTable.query.all()
    return records