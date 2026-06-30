from unittest.mock import patch, MagicMock

from app.tgbot import kafka_listener_format, kafka_listener, start


class TestKafkaListenerFormat:
    """Тест на формат данных"""
    def test_kafka_listener_format(self):
        result = kafka_listener_format({
            "id": "63c9f5e6-a6d3-4c53-8789-c4397d93b89e",
            "schema": "public",
            "table": "sales",
            "action": "INSERT",
            "data": {
                "about_partner": "123",
                "address": "123",
                "category": "Еда",
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

        expected = "[2026-06-26T08:20:07.704761Z] INSERT в таблице sales\nДанные: {'about_partner': '123', 'address': '123', 'category': 'Еда', 'company_name': '123', 'date_of_add': '2026-06-26', 'how_to_get': '123', 'id': 57, 'promo': '123', 'sale_name': '123', 'sale_period': '1111-11-11'}"
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
                "category": "Еда",
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


    def test_missing_action_returns_none(self):
        """Тест с данными без action"""
        result = kafka_listener_format({
            "table": "sales",
            "data": {"id": 1},
            "commitTime": "2026-06-26T08:20:07.704761Z",
        })
        assert result is None

    def test_insert_is_case_insensitive(self):
        """action сравнивается через .lower() поэтому "insert" в любом регистре должен сработать"""
        result = kafka_listener_format({
            "action": "insert",
            "table": "sales",
            "data": {"id": 1},
            "commitTime": "2026-06-26T08:20:07.704761Z",
        })
        assert result == "[2026-06-26T08:20:07.704761Z] INSERT в таблице sales\nДанные: {'id': 1}"

    def test_insert_without_data_uses_empty_dict(self):
        """Тест без данных"""
        result = kafka_listener_format({
            "action": "INSERT",
            "table": "sales",
            "commitTime": "2026-06-26T08:20:07.704761Z",
        })
        assert result == "[2026-06-26T08:20:07.704761Z] INSERT в таблице sales\nДанные: {}"


class TestStartHandler:
    """Тест /start"""

    def test_start_sends_welcome_message(self):
        fake_message = MagicMock()
        fake_message.chat.id = 12345

        with patch("app.tgbot.bot.send_message") as mock_send:
            start(fake_message)

        mock_send.assert_called_once_with(12345, "Бот запущен!")


class TestKafkaListener:
    """
    создаем фейковое сообщение от кафка, чтобы протестировать поведение
    """

    def _make_fake_message(self, value):
        msg = MagicMock()
        msg.value = value
        return msg

    def test_sends_message_for_insert_event(self):
        insert_event = {
            "action": "INSERT",
            "table": "sales",
            "data": {"id": 1},
            "commitTime": "2026-06-26T08:20:07.704761Z",
        }

        fake_consumer = [self._make_fake_message(insert_event)]

        with patch("app.tgbot.KafkaConsumer", return_value=fake_consumer) as mock_consumer_cls, \
             patch("app.tgbot.bot.send_message") as mock_send:
            kafka_listener()

        mock_consumer_cls.assert_called_once()
        mock_send.assert_called_once_with(
            814799097,
            "[2026-06-26T08:20:07.704761Z] INSERT в таблице sales\nДанные: {'id': 1}",
        )





