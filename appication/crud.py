import logging

from sqlalchemy.exc import SQLAlchemyError

from .models import MyTable
from .schemas import MyTableSchema
from .extensions import db
from marshmallow import ValidationError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')

file_handler = logging.FileHandler('logs/crud.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

schema = MyTableSchema()

def add(record):
    try:
        data = schema.load(record)
        db.session.add(data)
        db.session.commit()
        logger.info(f"Добавлена запись: {data.id}, данные={schema.dump(data)}")
        return data, None
    except ValidationError as err:
        logger.error(f"Ошибка при добавлении записи: {err}", exc_info=True)
        return None, err.messages
    except SQLAlchemyError as err:
        logger.error(f"Ошибка БД при добавлении: {err}", exc_info=True)
        return None, {"db_error": str(err)}

def delete(id):
    try:
        record = MyTable.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        logger.info(f"Запись ID={id} удалена, данные={schema.dump(record)}")
        return record, None
    except SQLAlchemyError as err:
        logger.error(f"Ошибка БД при удалении ID={id}: {err}", exc_info=True)
        return None, {"db_error": str(err)}

def edit(id, data):
    record = MyTable.query.get_or_404(id)
    try:
        edited_data = schema.load(data, partial=True)
        for key, value in edited_data.__dict__.items():
            if key != "_sa_instance_state":
                setattr(record, key, value)
        db.session.commit()
        logger.info(f"Запись ID={id} успешна обновлена: {schema.dump(data)}")
        return record, None
    except ValidationError as e:
        logger.error(f"Ошибка редактирования записи ID={id}: {e}", exc_info=True)
        return None, e.messages
    except SQLAlchemyError as err:
        logger.error(f"Ошибка БД при редактировании записи ID={id}: {err}", exc_info=True)

def list_records():
    records = MyTable.query.all()
    logger.info(f"Получен список записей: {len(records)} шт.")
    return records