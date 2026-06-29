from datetime import date, timedelta


class TestSalesPage:
    """Тесты для /sales"""

    def test_empty_state(self, client):
        """Если акций нет"""
        response = client.get("/sales")
        assert response.status_code == 200
        assert "Пока нет акций" in response.text

    def test_shows_categories_with_counts(self, client, make_sale):
        """Проверка счетчика категорий"""
        make_sale(category="food")
        make_sale(category="food")
        make_sale(category="clothes")

        response = client.get("/sales")

        assert response.status_code == 200
        assert "food (2)" in response.text
        assert "clothes (1)" in response.text

    def test_shows_sale_short_info_as_link(self, client, make_sale):
        """Тест можно ли перейти в подробную информацию /sales/offer/ нажав на акцию из /sales"""
        sale = make_sale(company_name="Фудзияма", sale_name="сет за 1000р")

        response = client.get("/sales")

        assert response.status_code == 200
        assert "Фудзияма" in response.text
        assert "сет за 1000р" in response.text
        assert f"/sales/offer/{sale.id}" in response.text

    def test_new_count_only_counts_today(self, client, make_sale):
        """Тест на верную проверку новых акций (должны оторажаться только сегоднешние акции)"""
        yesterday = str(date.today() - timedelta(days=1))
        make_sale(date_of_add=str(date.today()))
        make_sale(date_of_add=yesterday)

        response = client.get("/sales")

        assert response.status_code == 200
        assert "Новые (1)" in response.text


class TestNewSalesPage:
    """Тест при отсутствии новых акций"""
    def test_empty_when_no_sales_today(self, client, make_sale):
        yesterday = str(date.today() - timedelta(days=1))
        make_sale(date_of_add=yesterday)

        response = client.get("/sales/new")

        assert response.status_code == 200
        assert "пока нет акций" in response.text


class TestCategoryPage:
    """Тесты для /sales/category/{category}."""

    def test_filters_by_category(self, client, make_sale):
        make_sale(sale_name="Акция еды", category="food")
        make_sale(sale_name="Акция одежды", category="clothes")

        response = client.get("/sales/category/food")

        assert response.status_code == 200
        assert "Акция еды" in response.text
        assert "Акция одежды" not in response.text

    def test_unknown_category_returns_empty_list(self, client):
        response = client.get("/sales/category/несуществующая")

        assert response.status_code == 200
        assert "пока нет акций" in response.text


class TestOfferPage:
    """
    Тесты для /sales/offer/{sale_id} (полная информация об акции)
    """

    def test_shows_full_information(self, client, make_sale):
        sale = make_sale(
            company_name="Фудзияма",
            sale_name="сет за 1000р",
            how_to_get="Покажите купон на кассе",
            promo="UYUT15",
            address="ул. Цветочная, 5",
            about_partner="Уютное кафе в центре",
        )

        response = client.get(f"/sales/offer/{sale.id}")

        assert response.status_code == 200
        assert "Фудзияма" in response.text
        assert "Покажите купон на кассе" in response.text
        assert "UYUT15" in response.text
        assert "ул. Цветочная, 5" in response.text
        assert "Уютное кафе в центре" in response.text

    def test_nonexistent_offer_returns_404(self, client):
        """
        Тест на несуществующей акции
        expected 404
        """
        response = client.get("/sales/offer/999999")
        assert response.status_code == 404

