#!/bin/sh
apt-get update -y
apt-get upgrade -y
apt-get install fonts-dejavu python-pip python-pil python-numpy git ntpdate -y
pip install --upgrade pip setuptools wheel
pip install inky pytz
sudo timedatectl set-ntp True
