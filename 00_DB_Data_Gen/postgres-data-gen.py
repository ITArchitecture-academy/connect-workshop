#!/usr/bin/env python3

import argparse
import random
import time
from datetime import datetime, timedelta

import psycopg2

# Verbindung zur Datenbank herstellen
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="user",
    user="user",
    password="password"
)
cursor = connection.cursor()

asset_names = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headset", "Webcam", "Docking Station"]
asset_descriptions = ["Dell", "HP", "Lenovo", "Apple", "Samsung", "Logitech", "Microsoft"]


# Funktion zum Hinzufügen eines Assets
def add_asset():
    asset_name = random.choice(asset_names)
    description = random.choice(asset_descriptions)
    acquisition_date = datetime.now() - timedelta(days=random.randint(1, 365))
    purchase_price = round(random.uniform(10.0, 1000.0), 2)
    # Fetch location id from db
    cursor.execute("SELECT location_id FROM Locations")
    locations = cursor.fetchall()
    current_location_id = random.choice(locations)[0]
    employee_id = random.randint(1, 10)

    query = """
        INSERT INTO Assets
        (asset_name, description, acquisition_date, purchase_price, current_location_id, employee_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
         asset_name, description, acquisition_date, purchase_price, current_location_id, employee_id))
    connection.commit()


locations = ["Lager Hamburg", "Lager Berlin", "Lager München", "Lager Köln", "Lager Frankfurt",
             "Lager Stuttgart", "Lager Düsseldorf", "Lager Dortmund", "Lager Essen", "Lager Leipzig",
             "Lager Bremen", "Lager Dresden", "Lager Hannover", "Lager Nürnberg", "Lager Duisburg"]

cities = ["Hamburg", "Berlin", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf",
          "Dortmund", "Essen", "Leipzig"]


# Funktion zum Hinzufügen einer Lage
def add_location():
    location_name = random.choice(locations)
    address = f"{random.choice(['Straße', 'Gasse', 'Platz'])} {random.randint(100, 999)}"
    city = random.choice(cities)
    country = "Deutschland"

    query = """
        INSERT INTO Locations
        (location_name, address, city, country)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (location_name, address, city, country))
    connection.commit()


# Funktion zum Hinzufügen einer Asset-Bewegung
def add_assets_movement():
    # time in ms
    # Daten aus der Datenbank abrufen
    cursor.execute("SELECT asset_id FROM Assets")
    asset_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT location_id FROM Locations")
    location_ids = [row[0] for row in cursor.fetchall()]

    # Zufällige Auswahl von asset_id, from_location_id und to_location_id
    asset_id = random.choice(asset_ids)
    from_location_id = random.choice(location_ids)
    to_location_id = random.choice(location_ids)

    # Generiere zufälliges Datum zwischen 1. Januar 2023 und heute
    transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
    # Zufällige Notiz aus Liste auswählen
    notes = random.choice(["Asset wurde verschickt", "Asset wurde empfangen", "Asset wurde zurückgegeben"])

    # Employee ID zwischen 1 und 10
    employee_id = random.randint(1, 10)

    # Füge die Asset-Bewegung hinzu
    query = """
        INSERT INTO Assets_Movements
        (asset_id, from_location_id, to_location_id, transaction_date, notes, employee_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query,
                   (asset_id, from_location_id, to_location_id, transaction_date, notes, employee_id))
    connection.commit()


# Funktion zum Löschen einer zufälligen Location
def delete_location():
    cursor.execute("SELECT location_id FROM Locations")
    location_ids = cursor.fetchall()
    if location_ids:
        random_location_id = random.choice(location_ids)[0]
        delete_query = "DELETE FROM Locations WHERE location_id = %s"
        cursor.execute(delete_query, (random_location_id,))
        connection.commit()


# Funktion zum Löschen eines zufälligen Assets
def delete_asset():
    cursor.execute("SELECT asset_id FROM Assets")
    asset_ids = cursor.fetchall()
    if asset_ids:
        random_asset_id = random.choice(asset_ids)[0]
        delete_query = "DELETE FROM Assets WHERE asset_id = %s"
        cursor.execute(delete_query, (random_asset_id,))
        connection.commit()


# Funktion zum Löschen einer zufälligen Asset-Bewegung
def delete_assets_movement():
    cursor.execute("SELECT transaction_id FROM Assets_Movements")
    transaction_ids = cursor.fetchall()
    if transaction_ids:
        random_transaction_id = random.choice(transaction_ids)[0]
        delete_query = "DELETE FROM Assets_Movements WHERE transaction_id = %s"
        cursor.execute(delete_query, (random_transaction_id,))
        connection.commit()


# Funktion zum Bearbeiten einer zufälligen Location
def edit_location():
    cursor.execute("SELECT location_id FROM Locations")
    location_ids = cursor.fetchall()
    if location_ids:
        random_location_id = random.choice(location_ids)[0]
        new_location_name = random.choice(locations)
        update_query = "UPDATE Locations SET location_name = %s WHERE location_id = %s"
        cursor.execute(update_query, (new_location_name, random_location_id))
        connection.commit()


# Funktion zum Bearbeiten eines zufälligen Assets
def edit_asset():
    cursor.execute("SELECT asset_id FROM Assets")
    asset_ids = cursor.fetchall()
    if asset_ids:
        random_asset_id = random.choice(asset_ids)[0]
        new_asset_name = random.choice(asset_names)
        new_description = random.choice(asset_descriptions)
        update_query = "UPDATE Assets SET asset_name = %s, description = %s WHERE asset_id = %s"
        cursor.execute(update_query, (new_asset_name, new_description, random_asset_id))
        connection.commit()


# Funktion zum Bearbeiten einer zufälligen Asset-Bewegung
def edit_assets_movement():
    cursor.execute("SELECT transaction_id FROM Assets_Movements")
    transaction_ids = cursor.fetchall()
    if transaction_ids:
        random_transaction_id = random.choice(transaction_ids)[0]
        new_notes = f"New Notes {random_transaction_id}"
        update_query = "UPDATE Assets_Movements SET notes = %s WHERE transaction_id = %s"
        cursor.execute(update_query, (new_notes, random_transaction_id))
        connection.commit()


# Hauptfunktion für zufällige oder gezielte Aktion basierend auf Parametern
def perform_action(action_type, num_actions, wait_time):
    actions = []
    weights = []

    if action_type == "random":
        actions = [add_location, add_asset, add_assets_movement, edit_location, edit_asset, edit_assets_movement,
                   delete_location, delete_asset, delete_assets_movement]
        weights = [1, 2, 3, 1, 2, 1, 1, 2, 1]
    elif action_type == "add":
        actions = [add_location, add_asset, add_assets_movement]
        weights = [1, 2, 3]
    elif action_type == "edit":
        actions = [edit_location, edit_asset, edit_assets_movement]
        weights = [2, 2, 1]
    elif action_type == "delete":
        actions = [delete_location, delete_asset, delete_assets_movement]
        weights = [1, 2, 1]

    for _ in range(num_actions):
        if actions:
            action = random.choices(actions, weights=weights)[0]
            action()
            print(f"Ausgeführte Aktion: {action.__name__}")

        time.sleep(wait_time)


# Hauptfunktion
def main():
    # Kommandozeilenargumente parsen
    parser = argparse.ArgumentParser(description="Datenbankaktionen")
    parser.add_argument("action", choices=["random", "add", "edit", "delete"], help="Art der Aktion")
    parser.add_argument("count", type=int, help="Anzahl der Aktionen")
    parser.add_argument("--wait", type=float, default=1.0,
                        help="Wartezeit zwischen den Aktionen in Sekunden (Standard: 1.0)")
    args = parser.parse_args()

    action_type = args.action  # Aktionstyp: random, add, edit, delete
    num_actions = args.count  # Anzahl der Aktionen
    wait_time = args.wait  # Wartezeit zwischen den Aktionen in Sekunden

    perform_action(action_type, num_actions, wait_time)


if __name__ == "__main__":
    main()
