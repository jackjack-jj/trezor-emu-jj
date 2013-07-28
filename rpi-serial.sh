#!/bin/bash
# load kernel modules for spi communication
modprobe spi_bcm2708
modprobe spidev

# stop getty process interfering with serial port
pkill -STOP -f '.*getty.*ttyAMA0.*'

# chdir into script location
cd `dirname $0`

# run trezor daemon
python trezor/__init__.py -s -d -dt socket -dp 127.0.0.1:2000

# resume getty
pkill -CONT -f '.*getty.*ttyAMA0.*'
