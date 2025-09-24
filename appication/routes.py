from flask import request, jsonify, Blueprint

from .crud import (add, delete, edit, list_records)
from .report import (download_excel)
from .schemas import MyTableSchema

bp = Blueprint("main", __name__)
schema = MyTableSchema()

API_COMMANDS = {
    "records": ["add", "delete", "edit", "list", "download"]
}

@bp.route("/<string:path>/<string:command>", methods=["POST", "GET", "PUT", "DELETE"])
@bp.route("/<string:path>/<string:command>/<int:id>", methods=["PUT", "DELETE"])
def catcher(path, command, id=None):

    if path not in API_COMMANDS or command not in API_COMMANDS[path]:
        return jsonify({"error": "Путь или команда не найдены"}), 404

    if command == "add":
        record, errors = add(request.json)
        if errors:
            return jsonify({"errors": errors}), 400
        return jsonify(schema.dump(record)), 201

    if command == "delete":
        record, errors = delete(id)
        if errors:
            return jsonify({"errors": errors}), 404
        return jsonify({"message": "Запись удалена"}), 200

    if command == "edit":
        record, errors = edit(id, request.json)
        if errors:
            return jsonify({"errors": errors}), 400
        return jsonify(schema.dump(record)), 200

    if command == "list":
        records = list_records()
        return jsonify(schema.dump(records, many=True)), 200

    if command == "download":
        age_param = request.args.get("age", type=int)
        records = list_records()
        return download_excel(records, age_param)

