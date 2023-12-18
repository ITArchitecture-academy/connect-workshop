#!/usr/bin/env bash
set -e

# Write connect systemd service file

echo "Writing connect systemd service file"
cat << EOF > /etc/systemd/system/kafka-connect.service
[Install]
WantedBy=multi-user.target

[Unit]
Description=Kafka Connect

[Service]
Type=simple
ExecStart=/home/user/kafka/bin/connect-distributed.sh /home/user/training/config/worker.properties
Restart=on-failure
User=user
WorkingDirectory=/home/user
EOF

echo "Starting Kafka Connect…"
systemctl daemon-reload
systemctl enable kafka-connect
systemctl start kafka-connect

echo "Waiting 10s to finish booting"
sleep 10
curl -s -X GET http://localhost:8090/ | jq
echo "Happy Hacking!"
