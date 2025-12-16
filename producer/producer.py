import json
import uuid
from confluent_kafka import Producer

producer_config = {
    "bootstrap.servers": "kafka:9092",
    "acks": "all",
    "retries": 5,
}


producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(
            f"✅ Delivered to {msg.topic()} | "
            f"partition {msg.partition()} | "
            f"offset {msg.offset()}"
        )

def send_event(topic, payload):
    producer.produce(
        topic=topic,
        value=json.dumps(payload).encode("utf-8"),
        callback=delivery_report
    )
    producer.poll(0)

# Orders event
send_event("orders", {
    "order_id": str(uuid.uuid4()),
    "user": "Nate Oyekanlu",
    "item": "Ford f450",
    "quantity": 139
})

# Payments event
send_event("payments", {
    "payment_id": str(uuid.uuid4()),
    "order_amount": 2340987,
    "currency": "Euro",
    "status": "PAID"
})

# Shipping event
send_event("shipping", {
    "shipment_id": str(uuid.uuid4()),
    "carrier": "Shipping",
    "status": "DISPATCHED"
})

producer.flush()
