from datetime import date, timedelta


VALID_FORM_DATA = {
    "company_name": "Фудзияма",
    "sale_name": "сет за 1000р",
    "category": "food",
    "how_to_get": "пройдайте душу",
    "sale_period": str(date.today() + timedelta(days=30)),
    "about_partner": "Фудзияма суши",
    "promo": "UYUT15",
    "address": "ссылка типо",
}


class TestAdminGet:
    """ Тест формы в /admin """

    def test_form(self, client):
        response = client.get("/admin")

        assert response.status_code == 200
        assert "<form" in response.text
        assert 'name="company_name"' in response.text



class TestAdminPost:
    """Тест на создания записи в /admin"""

    def test_creates_sale_with_valid_data(self, client, db_session):
        import models

        response = client.post("/admin", data=VALID_FORM_DATA)

        assert response.status_code == 200
        assert "Запись добавлена" in response.text

        saved = db_session.query(models.Sale).filter_by(company_name="Фудзияма").first()
        assert saved is not None
        assert saved.sale_name == "сет за 1000р"
        assert saved.category == "food"
        assert saved.promo == "UYUT15"
        assert saved.date_of_add == str(date.today())

    def test_sale_period_is_saved_as_date(self, client, db_session):
        """
        sale_period в модели имеет тип данных DATE. Форма отдаёт строку
        admin.py должен сконвертировать её в datetime.date перед сохранением
        """
        import models

        target_date = date.today() + timedelta(days=45)
        data = dict(VALID_FORM_DATA)
        data["sale_period"] = str(target_date)

        response = client.post("/admin", data=data)

        assert response.status_code == 200
        saved = db_session.query(models.Sale).filter_by(company_name="Фудзияма").first()
        assert saved is not None
        assert saved.sale_period == target_date

    def test_invalid_sale_period_format_shows_error(self, client):
        """Тест на невалидных данных для даты, проверяем чтобы выдало ошибку, а не 500"""
        data = dict(VALID_FORM_DATA)
        data["sale_period"] = "не дата"

        response = client.post("/admin", data=data)

        assert response.status_code == 200
        assert "message-error" in response.text or "Ошибка" in response.text


    def test_missing_required_field_returns_422(self, client):
        """Тест с пустыми данными"""
        data = dict(VALID_FORM_DATA)
        del data["company_name"]
        response = client.post("/admin", data=data)
        assert response.status_code == 422

    def test_new_sale_appears_on_sales_page(self, client):
        """Тест появилась ли добавленная акция в /sales"""
        client.post("/admin", data=VALID_FORM_DATA)

        response = client.get("/sales")

        assert "Фудзияма" in response.text
        assert "food (1)" in response.text

    def test_database_error_shows_error_message(self, client):
        """
        Поле category ограничено 50 символами, проверка на вывод ошибки, а не 500
        """
        data = dict(VALID_FORM_DATA)
        data["category"] = "x" * 200

        response = client.post("/admin", data=data)

        assert response.status_code == 200
        assert "message-error" in response.text or "Ошибка" in response.text