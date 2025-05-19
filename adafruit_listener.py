import os
import django
import csv
from paho.mqtt.client import Client
import app_secrets

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remote_monitor.settings')
django.setup()

from live_data.models import WardReading, Ward, Microcontroller 

# Adafruit IO Credentials
AIO_USERNAME = app_secrets.AIO_USERNAME
AIO_KEY = app_secrets.AIO_KEY
WARD_TEMP_FEED = app_secrets.WARD_TEMP_FEED
WARD_HUMIDITY_FEED = app_secrets.WARD_HUMIDITY_FEED

CSV_FILE_PATH = "sensor_data.csv"

# Make sure the CSV has headers
if not os.path.exists(CSV_FILE_PATH):
    with open(CSV_FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ward_temperature", "ward_humidity"])

# Cache last known values
sensor_cache = {
    "temperature": None,
    "humidity": None
}

def on_connect(client, userdata, flags, rc):
    print("Connected to Adafruit IO")
    client.subscribe(WARD_TEMP_FEED)
    client.subscribe(WARD_HUMIDITY_FEED)

def on_message(client, userdata, msg):
    print(f"Received from {msg.topic}: {msg.payload.decode()}")
    try:
        value = float(msg.payload.decode())
        if msg.topic == WARD_TEMP_FEED:
            sensor_cache["temperature"] = value
        elif msg.topic == WARD_HUMIDITY_FEED:
            sensor_cache["humidity"] = value

        # Save to DB and CSV if both are present
        if sensor_cache["temperature"] is not None and sensor_cache["humidity"] is not None:
            # --- BEGIN: Assign correct Ward and Microcontroller ---
            # Set these identifiers to match your setup
            MICROCONTROLLER_IDENTIFIER = "Raspberry"  # <-- set this to your actual microcontroller identifier
            WARD_ID = 1  # <-- set this to your actual ward id (integer)
            try:
                micro = Microcontroller.objects.get(identifier=MICROCONTROLLER_IDENTIFIER)
                ward = Ward.objects.get(id=WARD_ID)
            except Exception as e:
                print("Error finding Ward or Microcontroller:", e)
                return
            # --- END: Assign correct Ward and Microcontroller ---
            WardReading.objects.create(
                ward=ward,
                microcontroller=micro,
                temperature=sensor_cache["temperature"],
                humidity=sensor_cache["humidity"]
            )

            # Append to CSV
            with open(CSV_FILE_PATH, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([sensor_cache["temperature"], sensor_cache["humidity"]])

            print("Saved to DB and CSV:", sensor_cache)

            # Reset
            sensor_cache["temperature"] = None
            sensor_cache["humidity"] = None

    except Exception as e:
        print("Error storing data:", e)

# Setup MQTT client
client = Client()
client.username_pw_set(AIO_USERNAME, AIO_KEY)
client.on_connect = on_connect
client.on_message = on_message

# Connect and listen
client.connect("io.adafruit.com", 1883, 60)
client.loop_forever()
