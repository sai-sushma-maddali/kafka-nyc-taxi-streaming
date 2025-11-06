import pandas as pd
from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

print("Kafka producer initialized successfully!")

# Load Parquet data into DataFrame
try:
    df = pd.read_parquet("yellow_tripdata_2025-09.parquet").head(20)
    print(f"Loaded Parquet file.")
except Exception as e:
    print("Error while reading the data:", e)
    exit(1)

# Stream each row as a Kafka message
for i, row in df.iterrows():
    message = row.to_dict()
    # Convert Timestamp fields to ISO strings
    for key, value in message.items():
        if isinstance(value, pd.Timestamp):
            message[key] = value.isoformat()

    try:
        producer.send('nyc_taxi', value=message)
        print(f"Sent trip {i + 1}")
    except Exception as e:
        print(f"Error sending row {i + 1}: {e}")
    
    time.sleep(5)  # simulate streaming delay
