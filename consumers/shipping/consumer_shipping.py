import json
import logging
import signal
from confluent_kafka import Consumer, KafkaException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("shipping-consumer")

consumer_config = {
    # ✅ ONLY broker listener
    "bootstrap.servers": "kafka:9092",

    "group.id": "shipping-service",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest",

    "session.timeout.ms": 10000,
    "max.poll.interval.ms": 300000,
}

consumer = Consumer(consumer_config)

running = True

def shutdown(sig, frame):
    global running
    logger.info("Shutdown signal received. Closing Shipping consumer...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

consumer.subscribe(["shipping"])
logger.info("Kafka Shipping Consumer started and subscribed to topic: shipping")

try:
    while running:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(msg.error())
            continue

        shipment = json.loads(msg.value().decode("utf-8"))

        logger.info(
            "Shipment update | shipment_id=%s | carrier=%s | status=%s",
            shipment.get("shipment_id"),
            shipment.get("carrier"),
            shipment.get("status"),
        )

        consumer.commit(message=msg, asynchronous=False)

except KafkaException as e:
    logger.exception(e)

finally:
    consumer.close()
