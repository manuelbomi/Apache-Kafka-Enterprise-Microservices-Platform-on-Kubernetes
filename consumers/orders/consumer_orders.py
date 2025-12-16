import json
import logging
import signal
from confluent_kafka import Consumer, KafkaException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("orders-consumer")

consumer_config = {
    # ✅ ONLY broker listener
    "bootstrap.servers": "kafka:9092",

    "group.id": "orders-service",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest",

    "session.timeout.ms": 10000,
    "max.poll.interval.ms": 300000,
}

consumer = Consumer(consumer_config)

running = True

def shutdown(sig, frame):
    global running
    logger.info("Shutdown signal received. Closing Kafka consumer...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

consumer.subscribe(["orders"])
logger.info("Kafka Orders Consumer started and subscribed to topic: orders")

try:
    while running:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        order = json.loads(msg.value().decode("utf-8"))

        logger.info(
            "Order received | order_id=%s | user=%s | item=%s | quantity=%s",
            order.get("order_id"),
            order.get("user"),
            order.get("item"),
            order.get("quantity"),
        )

        consumer.commit(message=msg, asynchronous=False)

except KafkaException as e:
    logger.exception(e)

finally:
    consumer.close()
