import pika
import json
import sys

AMQP_URL = "amqp://guest:guest@localhost:5672/%2F"
EXCHANGE = "rapido-dispatch"

NAME = sys.argv[1]
PATTERN = sys.argv[2]

params = pika.URLParameters(AMQP_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare topic exchange
channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="topic",
    durable=False
)

# Create a private queue for each driver
queue_name = f"driver-{NAME.lower()}"

channel.queue_declare(
    queue=queue_name,
    durable=False,
    auto_delete=True
)

# Bind queue to routing pattern
channel.queue_bind(
    exchange=EXCHANGE,
    queue=queue_name,
    routing_key=PATTERN
)

print(f"[{NAME}] Listening with pattern: {PATTERN}")


def receive_request(ch, method, properties, body):
    request = json.loads(body.decode())

    # Reject messages missing the zone field
    if "zone" not in request:
        print(f"[{NAME}] Rejected bad message: {request}")

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
        return

    # Process valid messages and acknowledge them
    print(f"[{NAME}] Processed: {request}")

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


# Manual acknowledgement enabled
channel.basic_consume(
    queue=queue_name,
    on_message_callback=receive_request,
    auto_ack=False
)

try:
    channel.start_consuming()

except KeyboardInterrupt:
    print(f"\nStopping {NAME}...")

finally:
    connection.close()