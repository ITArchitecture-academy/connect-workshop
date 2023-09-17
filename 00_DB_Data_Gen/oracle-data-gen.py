#!/usr/bin/env python3

import random
import time
from datetime import datetime, timedelta
import argparse


import oracledb

# Verbindung zur Datenbank herstellen
connection = oracledb.connect(user="c##dbzuser", password="dbz", dsn="localhost:1521/orclpdb1")

# Cursor erstellen
cursor = connection.cursor()


# Funktion zum Hinzufügen neuer Daten
def add_employee():
    # Generiere zufällige Daten für Employees
    # ID = Timestamp
    employee_id = int(time.time())

    first_name = random.choice(
        ["Noah", "Liam", "Elias", "Ben", "Paul", "Jonas", "Finn", "Leon", "Lukas", "Maximilian", "Luca", "Henry",
         "Emma", "Mia", "Hannah", "Emilia", "Sofia", "Anna", "Marie", "Mila", "Lina"])
    last_name = random.choice(
        ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
         "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris"])
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    # Wähle zufälliges Datum zwischen 2010-01-01 und heute
    hire_date = (datetime.now() - timedelta(days=random.randint(0, 3650))).strftime("%Y-%m-%d")
    department_id = random.randint(1, 10)

    # Füge neuen Mitarbeiter hinzu
    query = f"INSERT INTO Employees (employee_id, first_name, last_name, email, hire_date, department_id) VALUES (:employee_id, :first_name, :last_name, :email, TO_DATE(:hire_date,'YYYY-MM-DD'), :department_id)"
    cursor.execute(query, employee_id=employee_id, first_name=first_name, last_name=last_name, email=email,
                   hire_date=hire_date, department_id=department_id)
    connection.commit()


# Funktion zum Hinzufügen einer Transaktion (Transactions)
def add_transaction():
    # Wähle einen zufälligen Mitarbeiter
    cursor.execute("SELECT employee_id FROM Employees")
    employees = cursor.fetchall()
    employee_id = random.choice(employees)[0]

    # Generiere zufällige Daten für Transactions
    transaction_id = int(time.time())
    transaction_type = random.choice(["Purchase", "Sale"])
    transaction_date = datetime.now().strftime("%Y-%m-%d")
    amount = round(random.uniform(10.0, 100000.0), 2)

    # Füge neue Transaktion hinzu
    query = f"INSERT INTO Transactions (transaction_id, transaction_type, transaction_date, amount, employee_id) VALUES (:transaction_id, :transaction_type, TO_DATE(:transaction_date,'YYYY-MM-DD'), :amount, :employee_id)"
    cursor.execute(query, transaction_id=transaction_id, transaction_type=transaction_type,
                   transaction_date=transaction_date, amount=amount, employee_id=employee_id)
    connection.commit()


def edit_employee():
    # Daten für Mitarbeiter aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()

    # Zufälligen Mitarbeiter auswählen
    employee = random.choice(employees)
    employee_id = employee[0]
    department_id = random.randint(1, 10)  # Neuer Abteilungs-ID-Wert generieren

    # Mitarbeiterdaten aktualisieren
    query = f"UPDATE Employees SET department_id = :department_id WHERE employee_id = :employee_id"
    cursor.execute(query, department_id=department_id, employee_id=employee_id)
    connection.commit()


def edit_department():
    # Daten für Abteilungen aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    # Zufällige Abteilung auswählen
    department = random.choice(departments)
    department_id = department[0]
    # Standort aus liste deutscher Städte generieren
    new_location = random.choice(
        ["Berlin", "Hamburg", "München", "Köln", "Frankfurt", "Stuttgart", "Düsseldorf", "Dortmund", "Essen", "Leipzig",
         "Bremen", "Dresden", "Hannover", "Nürnberg", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn",
         "Münster"])

    # Abteilungsdaten aktualisieren
    query = f"UPDATE Departments SET location = :new_location WHERE department_id = :department_id"
    cursor.execute(query, new_location=new_location, department_id=department_id)
    connection.commit()


def edit_transaction():
    # Daten für Transaktionen aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Transactions")
    transactions = cursor.fetchall()

    if len(transactions) > 0:
        # Zufällige Transaktion auswählen
        transaction = random.choice(transactions)
        transaction_id = transaction[0]
        new_amount = round(random.uniform(10.0, 100000.0), 2)  # Neuer Betragswert generieren

        # Transaktionsdaten aktualisieren
        query = f"UPDATE Transactions SET amount = :new_amount WHERE transaction_id = :transaction_id"
        cursor.execute(query, new_amount=new_amount, transaction_id=transaction_id)
        connection.commit()
    else:
        print("Es sind keine Transaktionen vorhanden.")



# Funktion zum Löschen eines Mitarbeiters (Employees)
def delete_employee():
    # Daten für Mitarbeiter aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()

    if len(employees) > 0:
        # Zufälligen Mitarbeiter auswählen
        employee = random.choice(employees)
        employee_id = employee[0]

        # Mitarbeiter löschen
        query = f"DELETE FROM Employees WHERE employee_id = :employee_id"
        cursor.execute(query, employee_id=employee_id)
        connection.commit()
    else:
        print("Es sind keine Mitarbeiter vorhanden.")

# Funktion zum Löschen einer Transaktion (Transactions)
def delete_transaction():
    # Daten für Transaktionen aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Transactions")
    transactions = cursor.fetchall()

    if len(transactions) > 0:
        # Zufällige Transaktion auswählen
        transaction = random.choice(transactions)
        transaction_id = transaction[0]

        # Transaktion löschen
        query = f"DELETE FROM Transactions WHERE transaction_id = :transaction_id"
        cursor.execute(query, transaction_id=transaction_id)
        connection.commit()
    else:
        print("Es sind keine Transaktionen vorhanden.")

# Funktion zum Löschen einer Abteilung (Departments)
def delete_department():
    # Daten für Abteilungen aus der Datenbank abrufen
    cursor.execute("SELECT * FROM Departments")
    departments = cursor.fetchall()

    if len(departments) > 0:
        # Zufällige Abteilung auswählen
        department = random.choice(departments)
        department_id = department[0]

        # Abteilung löschen
        query = f"DELETE FROM Departments WHERE department_id = :department_id"
        cursor.execute(query, department_id=department_id)
        connection.commit()
    else:
        print("Es sind keine Abteilungen vorhanden.")


# Hauptfunktion für zufällige oder gezielte Aktion basierend auf Parametern
def perform_action(action_type, num_actions, wait_time):
    actions = []
    weights = []

    if action_type == "random":
        actions = [add_employee, edit_employee, delete_employee, add_transaction, edit_transaction, delete_transaction, delete_department]
        weights = [2, 2, 1, 3, 2, 1, 1]
    elif action_type == "add":
        actions = [add_employee, add_transaction]
        weights = [2, 3]
    elif action_type == "edit":
        actions = [edit_employee, edit_transaction, edit_department]
        weights = [2, 3, 1]
    elif action_type == "delete":
        actions = [delete_employee, delete_transaction, delete_department]
        weights = [2, 3, 1]

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
    parser.add_argument("--wait", type=float, default=1.0, help="Wartezeit zwischen den Aktionen in Sekunden (Standard: 1.0)")
    args = parser.parse_args()

    action_type = args.action  # Aktionstyp: random, add, edit, delete
    num_actions = args.count  # Anzahl der Aktionen
    wait_time = args.wait  # Wartezeit zwischen den Aktionen in Sekunden

    perform_action(action_type, num_actions, wait_time)

if __name__ == "__main__":
    main()
