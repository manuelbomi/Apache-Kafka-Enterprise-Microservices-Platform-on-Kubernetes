# Apache Kafka (KRaft Mode) Enterprise Microservices Platform with Kubernetes (Kind)

## Project Overview

This repository demonstrates a production-grade, enterprise-level event-driven microservices architecture built using:

- [x] Apache Kafka (KRaft mode, no Zookeeper)

- [x] Python microservices (Producers & Consumers)

- [x] Docker (containerized services)

- [x] Kubernetes (orchestration, scaling, resilience)

##### The system models a real-world enterprise workflow consisting of Orders, Payments, and Shipping domains communicating asynchronously via Kafka topics.

##### Each domain is implemented as a fully independent microservice, deployed and orchestrated using Kubernetes.

---

## Why Microservices Architecture?

#### ▩ <ins>Domain Isolation</ins>

##### Each business capability is isolated into its own microservice:

- orders-consumer

- payments-consumer

- shipping-consumer

- kafka-producer (event generator)

##### This mirrors real enterprise systems, where teams own specific domains independently.

---

#### ◙ <ins>Independent Deployment</ins>

##### Each microservice:

- Has its own Python code

- Has its own Dockerfile

---

##### ◙ <ins>Is deployed via its own Kubernetes Deployment or Job</ins>

##### This allows:

- Independent scaling

- Independent updates

- Fault isolation

- Loose Coupling via Kafka

---

#### ♣  <ins>Services never call each other directly</ins>.

##### Instead, they communicate asynchronously through Kafka topics:

- orders

- payments

- shipping

##### This eliminates tight coupling and enables:

- Horizontal scaling

- Replayability

- Resilience to failures

---

## Microservices Architecture Diagram

                        +-------------------+
                        |   Kafka Producer  |
                        |  (Job / Events)   |
                        +---------+---------+
                                  |
             -------------------------------------------------
             |                    |                         |
        +----v----+          +----v----+               +----v-----+
        | Orders  |          | Payments|               | Shipping |
        | Consumer|          | Consumer|               | Consumer |
        +----+----+          +----+----+               +----+-----+
             |                    |                         |
        orders topic         payments topic            shipping topic
             |                    |                         |
        +---------------------------------------------------------+
        |               Apache Kafka (3 Brokers, KRaft)           |
        |        StatefulSet, Persistent Storage, Replication     |
        +---------------------------------------------------------+

---

## Microservices Breakdown

#### <ins>Orders Service</ins>

Code: consumer_orders.py

- Containerized via Docker

- Consumes from orders topic

- Consumer group: orders-service

#### <ins>Payments Service</ins>

Code: consumer_payments.py

- Consumes from payments topic

- Handles financial events

- Consumer group: payments-service

#### <ins>Shipping Service</ins>

Code: consumer_shipping.py

- Consumes from shipping topic

- Tracks fulfillment lifecycle

#### <ins>Producer Job</ins>

Code: producer.py

- Runs as a Kubernetes Job

- Publishes events to all topics

- Simulates upstream enterprise systems (web apps, APIs, ERP systems)

---

## Why Apache Kafka?

#### ◑ Apache Kafka is the backbone of enterprise data platforms because it provides:

- High Throughput & Low Latency

- Millions of events per second with minimal overhead.

#### ▩ Durability & Fault Tolerance

- Replicated partitions

- Data persisted on disk

- Broker failures are tolerated

#### ◙ Replayability

Consumers can:

- Rewind offsets

- Reprocess historical data

- Recover from failures

#### ◑ Consumer Groups

##### Multiple instances of the same service can scale horizontally without duplicate processing.

---

## Why Kafka KRaft (No Zookeeper)?

#### This project uses pure Apache Kafka KRaft mode, not Bitnami or Zookeeper.

##### Benefits:

- Simpler architecture

- Fewer moving parts

- Official Kafka future direction

- Production-ready controller quorum

> [!TIP] 
> This is not a toy Kafka setup — it mirrors modern Kafka deployments.
> 
---

## Why Kubernetes?

#### Kubernetes is essential for enterprise-grade systems because it provides:

#### <ins>  Self-Healing</ins>

- Pods restart automatically

- Failed containers are replaced

#### <ins>  Horizontal Scaling</ins>

- Scale consumers independently

- Increase throughput without code changes

#### <ins>  Service Discovery</ins>

- Kafka accessed via stable service DNS (kafka:9092)

- No hard-coded IPs

#### <ins> Rolling Updates</ins>

- Zero-downtime deployments

- Safe consumer restarts

---

## Why Docker Desktop Still Counts as Enterprise-Grade?

#### While Docker Desktop is used locally, the architecture itself is 100% production-grade:

- Same Docker images run in cloud Kubernetes clusters

- Same manifests apply to EKS, GKE, AKS

- Same Kafka setup works on bare metal or cloud

#### Docker Desktop is simply a local control plane for learning, validation, and CI pipelines.

---

## Project Structure

```python
enterprise-kafka-platform-k8s/
│
├── kafka/
│   ├── kafka-bitnami.yaml        # Kafka StatefulSet (KRaft mode, 3 brokers)
│   └── kafka-service.yaml        # Headless service for broker discovery
│
├── consumers/
│   ├── orders/
│   │   ├── Dockerfile            # Orders consumer image (runs consumer_orders.py)
│   │   └── consumer_orders.py    # Orders domain Kafka consumer
|   |   └── requirements.txt
│   │
│   ├── payments/
│   │   ├── Dockerfile            # Payments consumer image (runs consumer_payments.py)
│   │   └── consumer_payments.py  # Payments domain Kafka consumer
|   |   └── requirements.txt
│   │
│   └── shipping/
│       ├── Dockerfile            # Shipping consumer image (runs consumer_shipping.py)
│       └── consumer_shipping.py  # Shipping domain Kafka consumer
|       └── requirements.txt
│
├── producer/
│   ├── Dockerfile                # Producer container image (runs producer.py)
│   └── producer.py               # Event publisher for orders, payments, shipping
|   └── requirements.txt
│
├── k8s/
│   ├── orders-consumer.yaml      # Orders Deployment (scalable replicas)
│   ├── payments-consumer.yaml    # Payments Deployment (scalable replicas)
│   ├── shipping-consumer.yaml    # Shipping Deployment (scalable replicas)
│   └── producer-job.yaml         # One-off Kafka producer Job
│
├── requirements.txt              # Shared Python dependencies for all services
│
└── README.md                     # Project overview, architecture, and instructions

```

---

## ❆ Deployment Guide (Step-by-Step)

#### ▩ Clean Previous Kafka State

##### Ensure that you have Docker Desktop running. Turn on the Kubernetes cluster (Kind) with at least 3 pods on the Docker Desktop.

##### Clone the project from here: https://github.com/manuelbomi/Apache-Kafka-Enterprise-Microservices-Platform-on-Kubernetes.git

##### cd to the rook of the project

---

#### Set up Docker images for producer and consumers

#### Each consumer and the producer need their own Docker image. Open your terminal in the root project folder.

####  Build Producer image

```python
cd producer
docker build -t kafka-producer:latest .
```

---

####  Build Consumers images

#### Do this for each consumer:

- Orders consumer

```python
cd ../consumers
docker build -t orders-consumer:latest -f Dockerfile .
```


- Payments consumer
  
```python
docker build -t payments-consumer:latest -f Dockerfile .
```


- Shipping consumer

```python
docker build -t shipping-consumer:latest -f Dockerfile .
```

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/ec66b756-acef-41af-baeb-b2bf97606f1a" />

---


##### On the PyCharm (or VSCode) terminal, at the root of the project, run the folloiwng codes

```python
kubectl delete statefulset kafka
kubectl delete pvc -l app=kafka
```

---

##### Verify Kafka Cluster Formation

```python
kubectl get pods -l app=kafka -w
kubectl logs kafka-0
kubectl logs kafka-1
kubectl logs kafka-2
```

##### Ensure all 3 brokers are running and the KRaft quorum is formed.

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/aff8eb35-25b6-4ef7-8c09-bb5cec384a3d" />

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/5a2c4d03-9358-4806-bb5c-f7e3d7e2b0a0" />

---

##### Verify Kafka Environment

```python
kubectl exec -it kafka-0 -- env | findstr KAFKA_CFG_ADVERTISED_LISTENERS
kubectl exec -it kafka-1 -- env | findstr KAFKA_CFG_ADVERTISED_LISTENERS
kubectl exec -it kafka-2 -- env | findstr KAFKA_CFG_ADVERTISED_LISTENERS
```

---

##### Create Kafka Topics

```python

kubectl exec -it kafka-0 -- \
/opt/kafka/bin/kafka-topics.sh \
--bootstrap-server kafka-0.kafka:9092 \
--create --topic orders --partitions 3 --replication-factor 3

kubectl exec -it kafka-0 -- \
/opt/kafka/bin/kafka-topics.sh \
--bootstrap-server kafka-0.kafka:9092 \
--create --topic payments --partitions 3 --replication-factor 3

kubectl exec -it kafka-0 -- \
/opt/kafka/bin/kafka-topics.sh \
--bootstrap-server kafka-0.kafka:9092 \
--create --topic shipping --partitions 3 --replication-factor 3

```

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/0bee5cc2-9c4e-4e4e-805e-27b9dc7f5a36" />

---

##### Deploy Consumer Microservices

```python
kubectl apply -f k8s/orders-consumer.yaml
kubectl apply -f k8s/payments-consumer.yaml
kubectl apply -f k8s/shipping-consumer.yaml
```

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/7621a298-83b4-4875-99c8-42e3be5cbbca" />

---

##### Deploy Producer Job

```python
kubectl apply -f k8s/producer-job.yaml
```
---

##### Observe Logs

```python
kubectl logs -f deploy/orders-consumer
kubectl logs -f deploy/payments-consumer
kubectl logs -f deploy/shipping-consumer
kubectl logs -f job/kafka-producer
```

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/ec5053d0-49c2-4219-b7c3-5e81c18c5605" />

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/bb5525aa-3ea3-4f76-98b3-a9eac0f8c6b7" />

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/db77dd6d-96af-4741-8748-4d37d5bad9e1" />

<img width="1280" height="720" alt="Image" src="https://github.com/user-attachments/assets/b9f05048-038e-46b1-ad80-01be688a05b0" />

---

##### Sanity Check: Broker Visibility 

```python
kubectl exec -it kafka-0 -- \
/opt/kafka/bin/kafka-broker-api-versions.sh \
--bootstrap-server kafka-0.kafka:9092

```

---

##### Restart Everything (in case of any isssues)

```python
kubectl rollout restart deploy/orders-consumer
kubectl rollout restart deploy/payments-consumer
kubectl rollout restart deploy/shipping-consumer
```

##### Producer restart:

```python
kubectl delete job kafka-producer
kubectl apply -f k8s/producer-job.yaml
```

---

#### Producer Event Examples
```python
send_event("orders", {
    "order_id": str(uuid.uuid4()),
    "user": "Alice Smith",
    "item": "Laptop",
    "quantity": 2
})

send_event("payments", {
    "payment_id": str(uuid.uuid4()),
    "order_amount": 1200,
    "currency": "USD",
    "status": "PAID"
})

send_event("shipping", {
    "shipment_id": str(uuid.uuid4()),
    "carrier": "UPS",
    "status": "DISPATCHED"
})
``` 

## Enterprise Use Cases

##### This architecture applies directly to:

- E-commerce platforms

- Financial transaction pipelines

- Event-driven data platforms

- Real-time analytics systems

- Supply chain orchestration

- Streaming ETL pipelines
---

## Why This Project Is Production-Grade

- Kafka KRaft (no Zookeeper)

- Replicated topics

- Consumer groups

- Graceful shutdown handling

- Kubernetes orchestration

- Stateless microservices

- Clean separation of concerns


---





### Thank you for reading
---

### **AUTHOR'S BACKGROUND**
### Author's Name:  Emmanuel Oyekanlu
```
Skillset:   I have experience spanning several years in data science, developing scalable enterprise data pipelines,
enterprise solution architecture, architecting enterprise systems data and AI applications,
software and AI solution design and deployments, data engineering, high performance computing (GPU, CUDA), machine learning,
NLP, Agentic-AI and LLM applications as well as deploying scalable solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com

Website:  http://emmanueloyekanlu.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```
[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)











