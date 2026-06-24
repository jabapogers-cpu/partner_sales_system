from kafka import KafkaConsumer
import json

# 1. Настройка Consumer
# Укажите адрес вашего Kafka-брокера и group_id
# group_id позволяет Kafka запоминать, какие сообщения уже прочитаны
consumer = KafkaConsumer(
    'public_sales',  # Имя вашего топика (schema_table)
    bootstrap_servers=['localhost:9092'],
    group_id='my-group',  # Идентификатор группы потребителей
    auto_offset_reset='earliest',  # Начинать читать с самого первого сообщения
    enable_auto_commit=True,  # Автоматически подтверждать прочитанные сообщения
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Декодируем JSON из wal-listener
)

print("Начинаю слушать топик 'public_sales'...")

# 2. Чтение сообщений в бесконечном цикле
try:
    for message in consumer:
        # message.value - это уже Python-словарь (благодаря десериализатору)
        event_data = message.value

        print(f"Получено событие: {event_data['Action']}")
        print(f"  Таблица: {event_data['Schema']}.{event_data['Table']}")
        print(f"  Данные: {event_data['Data']}")
        print("-" * 20)

        # Здесь вы можете обработать событие, например, сохранить в свою БД или обновить кэш.
        # Обработка события из Kafka

except KeyboardInterrupt:
    print("Остановка consumer...")
finally:
    consumer.close()  # Закрываем соединение