from app.tgbot import kafka_listener_format


def test_kafka_listener_format():
    # ПЕРВЫЙ ТЕСТ: INSERT
    result = kafka_listener_format({
        "id": "63c9f5e6-a6d3-4c53-8789-c4397d93b89e",
        "schema": "public",
        "table": "sales",
        "action": "INSERT",
        "data": {
            "about_partner": "123",
            "address": "123",
            "category": "food",
            "company_name": "123",
            "date_of_add": "2026-06-26",
            "how_to_get": "123",
            "id": 57,
            "promo": "123",
            "sale_name": "123",
            "sale_period": "1111-11-11"
        },
        "dataOld": {},
        "commitTime": "2026-06-26T08:20:07.704761Z"
    })

    expected = "[2026-06-26T08:20:07.704761Z] INSERT в таблице sales\nДанные: {'about_partner': '123', 'address': '123', 'category': 'food', 'company_name': '123', 'date_of_add': '2026-06-26', 'how_to_get': '123', 'id': 57, 'promo': '123', 'sale_name': '123', 'sale_period': '1111-11-11'}"
    assert result == expected

    # ВТОРОЙ ТЕСТ: UPDATE (ожидаем None)
    result = kafka_listener_format({
        "id": "63c9f5e6-a6d3-4c53-8789-c4397d93b89e",
        "schema": "public",
        "table": "sales",
        "action": "UPDATE",
        "data": {
            "about_partner": "123",
            "address": "123",
            "category": "food",
            "company_name": "123",
            "date_of_add": "2026-06-26",
            "how_to_get": "123",
            "id": 57,
            "promo": "123",
            "sale_name": "123",
            "sale_period": "1111-11-11"
        },
        "dataOld": {},
        "commitTime": "2026-06-26T08:20:07.704761Z"
    })

    expected = None
    assert result == expected