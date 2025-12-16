# Apache Kafka (KRaft Mode) Enterprise Microservices Platform with Kubernetes (Kind)

## Project Overview

CThis repository demonstrates a production-grade, enterprise-level event-driven microservices architecture built using:

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


