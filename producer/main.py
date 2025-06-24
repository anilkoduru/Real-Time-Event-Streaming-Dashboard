import requests, time, json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

GITHUB_EVENTS_URL = "https://api.github.com/events"

while True:
    try:
        res = requests.get(GITHUB_EVENTS_URL)
        events = res.json()
        for event in events[:5]: 
            kafka_event = {
                "user_id": event["actor"]["login"],
                "event_type": event["type"],
                "timestamp": event["created_at"],
                "repo": event["repo"]["name"]
            }
            print("Sending:", kafka_event)
            producer.send("user-events", kafka_event)
        time.sleep(10) 
    except Exception as e:
        print("Error fetching GitHub data:", e)
