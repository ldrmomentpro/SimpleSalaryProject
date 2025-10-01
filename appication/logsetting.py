import logging

from elasticsearch import Elasticsearch
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')

# logs in file
file_handler = logging.FileHandler('logs/crud.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

es = Elasticsearch('http://localhost:9200')

class ElasticSearchHandler(logging.Handler):
    def __init__(self, index_name="crud_logs"):
        super().__init__()
        self.index_name = index_name

    def emit(self, record):
        log_entry = self.format(record)
        try:
            es.index(index=self.index_name, document={
                "timestamp": datetime.utcnow(),
                "level": record.levelname,
                "logger": record.name,
                "message": log_entry
            })
        except Exception as err:
            print(f"Elasticsearch logging error: {err}")

es_handler = ElasticSearchHandler()
es_handler.setFormatter(formatter)
logger.addHandler(es_handler)