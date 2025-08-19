import os
import requests, time, json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=os.environ.get("KAFKA_BROKER","kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(7, 4, 0)
)

GITHUB_EVENTS_URL = os.environ.get("GITHUB_EVENTS_URL", "https://api.github.com/events")

while True:
    try:
        res = requests.get(GITHUB_EVENTS_URL)
        events = res.json()
        if isinstance(events, list): 
            for event in events[:5]:
                kafka_event = {
                    "user_id": event.get("actor", {}).get("login", "unknown"),
                    "event_type": event.get("type", "unknown"),
                    "timestamp": event.get("created_at", ""),
                    "repo": event.get("repo", {}).get("name", "")
                }
                print("Sending:", kafka_event)
                producer.send("user-events", kafka_event)
        else:
            print("GitHub API returned unexpected data:", events)
    except Exception as e:
        print("Error fetching GitHub data:", e)
