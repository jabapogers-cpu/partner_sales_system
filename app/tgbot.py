from kafka import KafkaConsumer
import json
import telebot
import threading


bot = telebot.TeleBot("8775693148:AAFc4TaVQSpzYwHduMv7bqw6KHU6G1umTe0")

def kafka_listener():
    """
    Читает обновления в Кафке
    выводит в консоль данные
    отпровляет сообщение об изменении в чат 814799097

    """
    consumer = KafkaConsumer(
        "wal_listener_events.public_sales",
        bootstrap_servers="127.0.0.1:9094",
        group_id="sales-consumer-group-v3",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )



    for message in consumer:
        event = message.value

        action = event.get("action", "").lower()
        table = event.get("table")
        event_time = event.get("commitTime")
        data = event.get("data", {})

        if action == "insert":
            text = f"[{event_time}] {action.upper()} в таблице {table}\nДанные: {data}"
            bot.send_message(814799097, text)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Бот запущен!")

if __name__ == "__main__":
    threading.Thread(target=kafka_listener, daemon=True).start()
    bot.polling(none_stop=True)