# MCZ Musa Home-Assistant addon

This addon will start a gateway between the stove's websocket protocol to home-assistant MQTT.
The code is based on the code written by the guys from the credits section below with modifications to make it a Home Assistant addon.

There are 2 ways to connect to the MCZ stove:
1. The stove is connected to the house wifi AP
2. The stove itself is acting as a wifi AP

The first option is being used when using the phone app to control the stove.
I use the second option to connect my home assistant to the stove.

## Installation

My HA is installed on a raspberry pi. The rpi is connected using a wired connection to my home network. In order to connect the rpi to the stove, need to get into 
the ssh addon's terminal and issue:

```bash

# check that wifi is on
nmcli radio

# find the stove's AP name
nmcli device wifi

# connect to that AP
nmcli device wifi connect <stove's bssid> password <wifi password>

# don't know why, by dhcp is not working and had to set manual ip
nmcli connection edit <stove connection>

## inside the nmcli
# set ipv4.addresses 192.168.120.10/24
# save

nmcli connection reload

nmcli connection down <stove connection>
nmcli connection up <stove connection>
```

After having a wifi connection to the stove need to install the addons:
1. Install the MQTT addon
2. Install this addon, configure and start

## Home Assistant
After finishing the installation, the addon will configure HA to have 2 new devices:
1. climate.stove - a climate device to display and control the stove state
2. sensor.stove - a sensor device with detailed status of the stove as attributes

## Credits

[nbordin](https://github.com/nbordin/mcz_musa) and [Chibald maestrogateway](https://github.com/Chibald/maestrogateway) and [Anthony-55](https://github.com/Anthony-55/maestro)


## Diclaimer

**If** anyone will ever use this code, I do not take any responsability. Do not play with fire.


## License

This project is licensed under the WTFPL License.
