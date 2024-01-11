import random
import time
import uuid
from datetime import datetime, timedelta

import psycopg2

INSERT_MAINTENANCE_SQL = '''
    INSERT INTO maintenance_logs
    (turbine_id, date, actions_performed, next_maintenance_date, maintenance_costs, remarks)
    VALUES (%s, CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP, %s, %s);
'''

INSERT_OUTBOX_SQL = '''
    INSERT INTO debezium_outbox
    (aggregatetype, aggregateid, type, payload, payloadid)
    VALUES (%s, %s, %s, %s::json, %s);
'''


def insert_data():
    actions = ["Oil change", "Blade inspection", "Gearbox replacement"]
    turbine_id = random.randint(1, 100)
    actions_performed = random.choice(actions)
    maintenance_costs = random.uniform(1000, 5000)
    remarks = f"Performed by technician #{random.randint(1, 10)}"
    next_maintenance_date = datetime.now() + timedelta(days=random.randint(30, 365))

    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="maintenance",
            user="user",
            password="password"
        )
        cur = conn.cursor()
        cur.execute(INSERT_MAINTENANCE_SQL,
                    (turbine_id, actions_performed, maintenance_costs, remarks))

        maintenance_id = cur.fetchone()[0]

        payload = f'''{{
            "turbineId": {turbine_id},
            "action": "{actions_performed}",
            "nextMaintenance": "{next_maintenance_date.strftime('%Y-%m-%d %H:%M:%S')}"
        }}'''
        payload_id = uuid.uuid4()
        cur.execute(INSERT_OUTBOX_SQL,
                    ("WindTurbine", str(turbine_id), "MaintenancePerformed", payload, str(payload_id)))

        conn.commit()
        print(f"Inserted maintenance log and outbox event for turbine {turbine_id}.")
        cur.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == "__main__":
    inserts_per_second = 1  # Configure the number of inserts per second here.

    while True:
        insert_data()
        time.sleep(1 / inserts_per_second)
