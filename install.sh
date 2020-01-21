# !/bin/bash

apt update && \
    apt install -y mosquitto mosquitto-clients && \
    systemctl enable mosquitto.service

pip3 install -r requirements.txt
cp -Rf musa /opt/

cp ./systemd/musa.service /etc/systemd/system
chmod a+x /etc/systemd/system/musa.service
systemctl daemon-reload
systemctl enable musa
