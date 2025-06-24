from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer(
    "user-events",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="dashboard-consumer",
    value_deserializer=lambda x: x.decode('utf-8')
)

es = Elasticsearch("http://localhost:9200")

print("Listening for Kafka events...")

for msg in consumer:
    try:
        event = json.loads(msg.value)
        print("Indexing:", event)
        es.index(index="user-events", document=event)
    except json.JSONDecodeError as e:
        print("Skipping bad message:", msg.value)