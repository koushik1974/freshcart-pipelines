import pika
import json
import random
import time
from datetime import datetime, timezone

AMQP_URL = "amqp://guest:guest@localhost:5672/%2F"
EXCHANGE = "rapido-dispatch"

CITIES = ["bangalore", "chennai"]
ZONES = ["koramangala", "indiranagar", "whitefield", "tnagar"]
TYPES = ["ride", "food"]

params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare topic exchange
channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="topic",
    durable=False
)

print(f"Dispatcher publishing to '{EXCHANGE}'")

request_id = 0

try:
    while True:
        city = random.choice(CITIES)
        zone = random.choice(ZONES)
        typ = random.choice(TYPES)

        routing_key = f"{city}.{zone}.{typ}"

        request_id += 1

        # Create request
        request = {
            "id": request_id,
            "city": city,
            "zone": zone,
            "type": typ,
            "ts": datetime.now(timezone.utc).strftime("%H:%M:%S")
        }

        # Send one bad message every 10 messages
        if request_id % 10 == 0:
            request.pop("zone")

            print(f"Sending BAD message (missing zone): {request}")

        # Publish message
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(request).encode(),
            properties=pika.BasicProperties(
                content_type="application/json"
            )
        )

        print(f"Sent: {routing_key} -> {request}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping dispatcher...")

finally:
    connection.close()