#!/usr/bin/env python3
"""
consumer_payments.py

Enterprise-grade Kafka consumer for the Payments domain.

This service consumes payment events from the `payments` Kafka topic
using a dedicated consumer group. It is designed to scale horizontally
and process financial events reliably.

Kafka:
- Multi-broker (KRaft mode)
- Topic: payments
- Consumer Group: payments-service
"""

import json
import logging
import signal
from confluent_kafka import Consumer, KafkaException

# -------------------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("payments-consumer")

# -------------------------------------------------------------------------------
# Kafka Consumer Configuration
# -------------------------------------------------------------------------------

consumer_config = {
    # ✅ Only broker listener
    "bootstrap.servers": "kafka:9092",

    "group.id": "payments-service",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest",

    "session.timeout.ms": 10000,
    "max.poll.interval.ms": 300000,
}

consumer = Consumer(consumer_config)

# -------------------------------------------------------------------------------
# Graceful Shutdown Handling
# -------------------------------------------------------------------------------

running = True

def shutdown(signal_received, frame):
    global running
    logger.info("Shutdown signal received. Closing Payments consumer...")
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# -------------------------------------------------------------------------------
# Subscription
# -------------------------------------------------------------------------------

consumer.subscribe(["payments"])
logger.info("Kafka Payments Consumer started and subscribed to topic: payments")

# -------------------------------------------------------------------------------
# Message Processing Loop
# -------------------------------------------------------------------------------

try:
    while running:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue

        if msg.error():
            logger.error(f"Kafka error: {msg.error()}")
            continue

        payment = json.loads(msg.value().decode("utf-8"))

        logger.info(
            "Payment received | payment_id=%s | amount=%s %s | status=%s",
            payment.get("payment_id"),
            payment.get("order_amount"),
            payment.get("currency"),
            payment.get("status"),
        )

        consumer.commit(message=msg, asynchronous=False)

except KafkaException as e:
    logger.exception(f"Kafka exception occurred: {e}")

finally:
    logger.info("Closing Payments consumer")
    consumer.close()
