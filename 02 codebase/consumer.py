from kafka import KafkaConsumer
import json
import pandas as pd

# Initialize Kafka consumer
consumer = KafkaConsumer(
    "nyc_taxi",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest'
)

# reading location data and converting to dictionary
loc_df = pd.read_csv("taxi_zone_lookup.csv")
loc_dict = dict(zip(loc_df["LocationID"], loc_df["Zone"]))

# Defining payment method dictionary
payment_type_map = {
    0: "Flex Fare trip",
    1: "Credit card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided trip"
}


for message in consumer:
    data = message.value
    try:
        pickup_loc = loc_dict.get(data["PULocationID"], "Unknown")
        drop_loc = loc_dict.get(data["DOLocationID"],"Unknown")
        
        pickup_time = pd.to_datetime(data["tpep_pickup_datetime"])
        drop_time = pd.to_datetime(data["tpep_dropoff_datetime"])
        
        trip_duration = round((drop_time - pickup_time) / pd.Timedelta(minutes=1), 0)
        trip_speed = round(data["trip_distance"] / (trip_duration / 60), 2) if trip_duration > 0 else 0
        payment_method = payment_type_map.get(data["payment_type"],"Other")
        total_amount = data["total_amount"]
        print(f"Trip from {pickup_loc} to {drop_loc}, duration: {trip_duration} mins, trip_speed: {trip_speed} mph, total_amount: $ {total_amount}, payment_method: {payment_method}\n")
    except Exception as e:
        print("Error processing message", e)
