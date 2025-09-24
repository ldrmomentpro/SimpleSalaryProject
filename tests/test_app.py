from appication import create_app
from appication.extensions import db
from appication.models import MyTable, City, Country, SalaryGrade
from datetime import date
import unittest


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        if not self.app.config.get("TESTING", False):
            raise RuntimeError("drop_all запрещен без TESTING=True")
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database_connection(self):
        with self.app.app_context():
            result = db.session.execute(db.text("SELECT 1")).scalar()
            self.assertEqual(result, 1, "Не удалось выполнить соединение")

    def test_add_record(self):
        test_user = {
            "first_name": "John",
            "last_name": "Wick",
            "email": "johnwick@gmail.com",
            "phone": "+99612345678",
            "birth_date": "1990-01-01",
            "city_id": 1,
            "salary_grade_id": 1
        }

        with self.app.app_context():
            from appication.models import City, SalaryGrade
            city = City(id=1, name="Бишкек", country_id=1)
            grade = SalaryGrade(grade=1, amount=10000)
            db.session.add(city)
            db.session.add(grade)
            db.session.commit()

        response = self.client.post('/records/add', json=test_user)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['email'], "johnwick@gmail.com")

    def test_list_records(self):
        with self.app.app_context():
            record = MyTable(
                first_name="John",
                last_name="Wick",
                email="johnwick@gmail",
                phone="+99612345678",
                birth_date=date(1990,1,1),
                city_id=1,
                salary_grade_id=1,
            )
            db.session.add(record)
            db.session.commit()

        response = self.client.get('/records/list')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "first_name" in data[0]

    def test_edit_record(self):
        with self.app.app_context():
            test_user = MyTable(
                first_name="John",
                last_name="Wick",
                email="johnwick@gmail",
                phone="+99612345678",
                birth_date=date(1990, 1, 1),
                city_id=1,
                salary_grade_id=1,
            )

            db.session.add(test_user)
            db.session.commit()

            edited_user = {"first_name": "Kenny"}
            response = self.client.put(f"/records/edit/{test_user.id}", json=edited_user)
            assert response.status_code == 200
            data = response.get_json()
            assert data["first_name"] == "Kenny"

    def test_delete_record(self):
        with self.app.app_context():
            test_user = MyTable(
                first_name="John",
                last_name="Wick",
                email="johnwick@gmail",
                phone="+99612345678",
                birth_date=date(1990, 1, 1),
                city_id=1,
                salary_grade_id=1,
            )
            db.session.add(test_user)
            db.session.commit()

            response = self.client.delete(f"/records/delete/{test_user.id}")
            assert response.status_code == 200
            data = response.get_json()
            assert "Запись удалена" in data["message"]

    def test_download_excel(self):
        with self.app.app_context():
            test_user = MyTable(
                first_name="John",
                last_name="Wick",
                email="johnwick@gmail",
                phone="+99612345678",
                birth_date=date(1990, 1, 1),
                city_id=1,
                salary_grade_id=1,
            )
            db.session.add(test_user)
            db.session.commit()

            response = self.client.get("/records/download")
            assert response.status_code == 200
            assert response.mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            assert len(response.data) > 0

if __name__ == '__main__':
    unittest.main()