# Real-Time NYC Taxi Trip Data Processing with Apache Kafka

## **Project Overview**

This project demonstrates a **real-time data streaming and processing pipeline** built using **Apache Kafka** and **Python**, applied to the **NYC Yellow Taxi dataset**.

The pipeline streams trip records from a Parquet file to Kafka and processes each trip in real time to compute **trip duration**, **average speed**, **payment method**, and **pickup/drop-off zones** using lookup data.

This simulates how large-scale transportation systems monitor trip metrics live for insights, alerts, or dashboards.

---
## Demo Recording

[Click here to watch the demo](https://github.com/user-attachments/assets/570cb2be-5b1f-4312-8475-b4bf8fcb4b02)

> The video demonstrates the end-to-end Kafka streaming pipeline — the producer streams trip records and the consumer performs real-time analytics on trip data.

---

## **Pipeline Architecture**

```
+-----------------------+         +-------------------------+         +--------------------------+
|   Parquet Data File   |  --->   |     Kafka Producer      |  --->   |       Kafka Topic        |
| (yellow_tripdata_2025)|         | (Streams trip records)  |         |     ('nyc_taxi')         |
+-----------------------+         +-------------------------+         +-----------+--------------+
                                                                              |
                                                                              v
                                                                 +-----------------------------+
                                                                 |     Kafka Consumer          |
                                                                 | (Computes metrics:          |
                                                                 |  duration, speed, payment)  |
                                                                 +-----------------------------+
```

---

## **Data Source**

* **Dataset:** [NYC Yellow Taxi Trip Records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
* **Files Used:**

  * `yellow_tripdata_2025-09.parquet` — sample trip data used for the project
  * `taxi_zone_lookup.csv` — mapping of location IDs to borough/zone names

Each record represents a single taxi trip with timestamps, distance, amount, and payment details.

---

## **Producer — `producer.py`**

### **Functionality**

* Reads the trip rows of the Parquet file.
* Converts each row to JSON and streams it into Kafka topic **`nyc_taxi`**.
* Converts timestamps to ISO strings for serialization.
* Simulates continuous trip data using `time.sleep(5)` delay.

---

## **Consumer — `consumer.py`**

### **Functionality**

* Subscribes to Kafka topic **`nyc_taxi`**.
* Reads trip data in real time and computes:

  * **Pickup and Drop-off Zone** (using `taxi_zone_lookup.csv`)
  * **Trip Duration** in minutes
  * **Average Speed** (distance / duration)
  * **Payment Method** (mapped from payment_type)
  * **Total Fare Amount**

### **Example Output**

```
Trip from Midtown East to JFK Airport, duration: 45 mins, trip_speed: 32.5 mph,
total_amount: $65.0, payment_method: Credit card
```

### **Data Enrichment Dictionaries**

* **Location Mapping:**
  Converts LocationID → Zone name using `taxi_zone_lookup.csv`
* **Payment Type Mapping:**

  ```
  1: Credit card
  2: Cash
  3: No charge
  4: Dispute
  5: Unknown
  6: Voided trip
  ```

---

## **Technologies Used**

| Component        | Purpose                                               |
| ---------------- | ----------------------------------------------------- |
| **Apache Kafka** | Real-time data streaming and message queue            |
| **Python**       | Producer and consumer implementation                  |
| **Pandas**       | Data parsing, timestamp handling, and transformations |
| **JSON**         | Message serialization                                 |
| **Kafka-Python** | Kafka API client library                              |

---

## **How to Run the Project**

### **Step 1 — Start Zookeeper and Kafka**

```bash
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties
```

### **Step 2 — Create Kafka Topic**

```bash
kafka-topics.sh --create --topic nyc_taxi \
--bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### **Step 3 — Run the Producer**

```bash
python3 producer.py
```

### **Step 4 — Run the Consumer**

```bash
python3 consumer.py
```

You’ll see real-time trip summaries printed to the console.

---

## **Example Output**

```
Trip from Chelsea to JFK Airport, duration: 42 mins, trip_speed: 28.6 mph, 
total_amount: $58.5, payment_method: Credit card

Trip from Times Sq/Theatre District to Upper West Side South, duration: 12 mins, 
trip_speed: 21.2 mph, total_amount: $18.0, payment_method: Cash
```
---

## **Environment and Dependencies**

| Library      | Version |
| ------------ | ------- |
| Python       | 3.10    |
| kafka-python | 2.0.2   |
| pandas       | 2.2.3   |

---

## **Project Files**

| File                              | Description                                    |
| --------------------------------- | ---------------------------------------------- |
| `producer.py`                     | Kafka producer that streams trip data          |
| `consumer.py`                     | Kafka consumer that processes trip data        |                       |
| `taxi_zone_lookup.csv`            | Zone name mapping for pickup/dropoff locations |
| `README.md`                       | Project documentation                          |

---

## **Conclusion**

This project demonstrates how **Apache Kafka** can be integrated with **Python and real-world data** to process high-velocity streaming data efficiently.
The pipeline can be extended for advanced analytics such as **anomaly detection**, **ETA prediction**, or **real-time fare optimization**, making it ideal for large-scale transportation data systems.


