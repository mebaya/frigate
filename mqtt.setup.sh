#!/bin/bash
#

sudo apt install mosquitto mosquitto-clients -y
sudo cp mqtt_build/mosquitto.pass /etc/mosquitto/passwd

sudo cp mqtt_build/mosquitto.conf /etc/mosquitto/mosquitto.conf
sudo systemctl start mosquitto
