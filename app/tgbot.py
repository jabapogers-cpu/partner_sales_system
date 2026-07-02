from kafka import KafkaConsumer
import json
import telebot
import threading
import configtg

token: str = configtg.token
bot: telebot.TeleBot = telebot.TeleBot(token)


def kafka_listener_format(event: dict) -> str | None:
    """
    Форматирует событие из Kafka в текст для Telegram.
    Возвращает строку для INSERT, None для прочих событий.
    """
    action: str = event.get("action", "").lower()
    table: str | None = event.get("table")
    event_time: str | None = event.get("commitTime")
    data: dict = event.get("data", {})

    if action == "insert":
        return f"[{event_time}] {action.upper()} в таблице {table}\nДанные: {data}"

    return None


def kafka_listener() -> None:
    """
    Читает события из Kafka-топика и отправляет уведомления в Telegram.
    Обрабатывает только INSERT-события; UPDATE/DELETE молча пропускаются.
    """
    consumer: KafkaConsumer = KafkaConsumer(
        "wal_listener_events.public_sales",
        bootstrap_servers="127.0.0.1:9094",
        group_id="sales-consumer-group-v3",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    for message in consumer:
        event: dict = message.value
        text: str | None = kafka_listener_format(event)
        if text:
            bot.send_message(814799097, text)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, "Бот запущен!")


if __name__ == "__main__":
    threading.Thread(target=kafka_listener, daemon=True).start()
    bot.polling(none_stop=True)