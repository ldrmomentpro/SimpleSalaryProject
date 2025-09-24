Flask CRUD + Excel API

Этот проект – REST API на Flask для управления записями в таблице поддержкой:
•	Добавление, редактирование, удаление и листинга данных
•	Скачивания данных в Excel


Стек технологий

•	Python – язык программирования
•	Flask — веб-фреймворк
•	SQLAlchemy — работа с БД
•	Flask-Migrate — миграции
•	Marshmallow — валидация данных
•	Pandas — генерация Excel
•	[pytest / unittest] — тестирование API


Установка и запуск

1)	Клонируй репозиторий:
git clone https://github.com/ldrmomentpro/SimpleSalaryProject.git
2)	Установи зависимости:
pip install -r requirements.txt
3)	Создай базу данных и сделай миграции:
flask db init
flask db migrate -m "initial"
flask db upgrade
4)	Запусти сервер:
flask run
5)	API будет доступно по адресу:
http://127.0.0.1:5000/


Примеры API запросов:

1)	Добавление:
POST http://127.0.0.1:5000/records/add
2)	Редактирование:
PUT http://127.0.0.1:5000/records/edit/<id>
3)	Удаление:
DELETE http://127.0.0.1:5000/records/delete/<id>
4)	Получение списка всей записей:
GET http://127.0.0.1:5000/records/list
5)	Скачивание в Excel:
http://127.0.0.1:5000/records/download
Если нужна фильтрация по возрасту:
http://127.0.0.1:5000/records/download?age=<int:age>
Запуск тестов
•	pytest -v


Структура проекта

SimpleSalaryProject/
│
├── app/
│   ├── __init__.py         # Создание приложения Flask
│   ├── models.py           # SQLAlchemy модели
│   ├── schemas.py          # Marshmallow схемы
│   ├── routes.py           # API endpoints (Blueprint)
│   ├── crud.py             # Логика add/edit/delete/list
│   ├── report.py           # Генерация Excel
│   └── utils.py            # Утилиты
│
├── tests/
│   └── test_routes.py      # Тесты API
│
├── migrations/             # Flask-Migrate файлы
├── requirements.txt
└── README.md               #  Документация
