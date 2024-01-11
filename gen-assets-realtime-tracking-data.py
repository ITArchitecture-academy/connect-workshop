#!/usr/bin/env python3
import json
import random
import sys
import time
from datetime import datetime

""""
Format of the data in the Kafka topic `assets_realtime_tracking`:
Key: asset_id
Value: JSON Object with the Schema and the payload as follows:
"""

# Schema
schema = {
    "type": "struct",
    "fields": [
        {
            "field": "asset_id",
            "type": "string"
        },
        {
            "field": "asset_type",
            "type": "string"
        },
        {
            "field": "asset_status",
            "type": "string"
        },
        {
            "field": "asset_position_lat",
            "type": "float"
        },
        {
            "field": "asset_position_lon",
            "type": "float"
        },
        {
            "field": "timestamp",
            "type": "string"
        }
    ]
}

asset_types = ["laptop", "smartphone", "tablet", "smartwatch", "smartglasses", "drone", "robot", "sensor", "camera",
               "server"]
asset_statuses = ["active", "inactive", "broken", "lost", "stolen"]

last_state = {}


def gen_data(asset_id):
    if asset_id not in last_state:
        asset_type = random.choice(asset_types)
        asset_status = random.choice(asset_statuses)
        asset_position_lat = random.uniform(-90, 90)
        asset_position_lon = random.uniform(-180, 180)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_state[asset_id] = {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "asset_status": asset_status,
            "asset_position_lat": asset_position_lat,
            "asset_position_lon": asset_position_lon,
            "timestamp": timestamp
        }
    else:
        last_state[asset_id]["asset_position_lat"] += random.uniform(-0.1, 0.1)
        last_state[asset_id]["asset_position_lon"] += random.uniform(-0.1, 0.1)
        last_state[asset_id]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return last_state[asset_id]


num_assets = 50
while True:
    asset_num = random.randint(1, num_assets)
    asset_id = "asset_" + str(asset_num)
    payload = gen_data(asset_id)
    json_data = json.dumps({"schema": schema, "payload": payload})
    print(asset_id + ":" + json_data)
    sys.stdout.flush()
    time.sleep(1)
