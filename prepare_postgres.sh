#!/usr/bin/env bash

echo "Creating database and user \`user\`"
sudo -u postgres psql << EOF
CREATE DATABASE "user";
CREATE ROLE "user" LOGIN PASSWORD 'password';
ALTER DATABASE "user" OWNER TO "user";
EOF

echo "Creating tables"

psql << EOF
CREATE TABLE Locations (
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(255),
    address VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE Assets (
    asset_id SERIAL PRIMARY KEY,
    asset_name VARCHAR(255),
    description VARCHAR(255),
    acquisition_date DATE,
    purchase_price DECIMAL(10, 2),
    current_location_id INTEGER,
    employee_id INTEGER,
    FOREIGN KEY (current_location_id) REFERENCES Locations(location_id) ON DELETE CASCADE
);

CREATE TABLE Assets_Movements (
    transaction_id SERIAL PRIMARY KEY,
    asset_id INTEGER,
    from_location_id INTEGER,
    to_location_id INTEGER,
    transaction_date DATE,
    notes VARCHAR(255),
    employee_id INTEGER,
    FOREIGN KEY (asset_id) REFERENCES Assets(asset_id) ON DELETE CASCADE,
    FOREIGN KEY (from_location_id) REFERENCES Locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (to_location_id) REFERENCES Locations(location_id) ON DELETE CASCADE
);
EOF

echo "Inserting data"

psql << EOF
INSERT INTO Locations (location_name, address, city, country) VALUES
('Lager Hamburg', 'Musterstraße 1', 'Hamburg', 'Deutschland'),
('Lager Berlin', 'Beispielweg 2', 'Berlin', 'Deutschland'),
('Lager München', 'Testgasse 3', 'München', 'Deutschland'),
('Lager Köln', 'Musterplatz 4', 'Köln', 'Deutschland'),
('Lager Frankfurt', 'Beispielallee 5', 'Frankfurt', 'Deutschland'),
('Lager Stuttgart', 'Teststraße 6', 'Stuttgart', 'Deutschland'),
('Lager Düsseldorf', 'Musterweg 7', 'Düsseldorf', 'Deutschland'),
('Lager Hannover', 'Beispielpfad 8', 'Hannover', 'Deutschland'),
('Lager Leipzig', 'Testplatz 9', 'Leipzig', 'Deutschland'),
( 'Lager Nürnberg', 'Musterpfad 10', 'Nürnberg', 'Deutschland');

INSERT INTO Assets (asset_name, description, acquisition_date, purchase_price, current_location_id, employee_id) VALUES
('Laptop 1', 'Acer TravelMate', '2023-01-01', 899.99, 1, 1),
('Desktop-Computer 1', 'Dell OptiPlex', '2023-01-02', 1299.99, 2, 2),
('Drucker 1', 'HP LaserJet', '2023-01-03', 299.99, 1, 3),
('Monitor 1', 'Samsung Curved', '2023-01-04', 449.99, 3, 4),
('Server 1', 'IBM Power System', '2023-01-05', 4999.99, 2, 5),
('Smartphone 1', 'Samsung Galaxy', '2023-01-06', 799.99, 1, 6),
('Tablet 1', 'Apple iPad', '2023-01-07', 599.99, 3, 7),
('Kamera 1', 'Canon EOS', '2023-01-08', 1499.99, 1, 8),
('Projektor 1', 'Epson PowerLite', '2023-01-09', 899.99, 2, 9),
('Drohne 1', 'DJI Phantom', '2023-01-10', 1299.99, 3, 10);

-- Asset 1
INSERT INTO Assets_Movements (asset_id, from_location_id, to_location_id, transaction_date, notes, employee_id) VALUES
(1, 1, 2, '2023-01-01', 'Umlagerung von Lager 1 nach Lager 2', 1),
(1, 2, 3, '2023-02-03', 'Optimierung der Lagerplatznutzung', 2),
(1, 3, 1, '2023-03-05', 'Rückverlagerung von Lager 3 nach Lager 1', 3);

-- Asset 2
INSERT INTO Assets_Movements (asset_id, from_location_id, to_location_id, transaction_date, notes, employee_id) VALUES
(2, 1, 3, '2023-01-02', 'Umlagerung von Lager 1 nach Lager 3', 4),
(2, 3, 2, '2023-02-04', 'Optimierung der Lagerplatznutzung', 5);

-- Asset 3
INSERT INTO Assets_Movements (asset_id, from_location_id, to_location_id, transaction_date, notes, employee_id) VALUES
(3, 2, 1, '2023-01-03', 'Umlagerung von Lager 2 nach Lager 1', 6);
EOF