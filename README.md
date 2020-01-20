# MCZ Musa Maestro Python Controller

This program allows controlling remotely your **MCZ Musa** pellet stove and retrieve its status. MCZ Musa Maestro Python Controller uses a MQTT broker to receive JSON commands, convert and send them to the MCZ Musa through a Web Socket connection.

<div style="text-align:center;"><img src="./assets/mcz_musa.jpg"/></div>

It has been tested on MCZ Musa Suite Comfort Air 12 M1.


## Installation

To run MCZ Musa Maestro Python Controller your smart home gateway device connection must be bridged between the stove internal Wi-Fi and your local network. It can be achieved easily with a Raspberry Pi device and, if an Ethernet port is not available, a (Micro) USB-Ethernet adapter.

The first step is installing a MQTT message broker, for example [Mosquitto](https://mosquitto.org/download/).

Install, then, `python3.7+` dependencies with

```bash
sudo apt install python3-pip
pip3 install -r requirements.txt
```

After connecting to the stove's Wi-Fi, run

```
python3 musa
```


### Containerization

An alternative to MCZ Musa Maestro Python Controller installation is its `docker` containerization, with lightweight Alpine images. It requires the installation of [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/). For Raspberry PI see [Raspberry PI Docker Installation Guide](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl).


After the installation and the connection of your device with the stove's Wi-Fi, simply run the MQTT broker and the Python Controller with

```bash
# download eclipse-mosquitto base image
docker pull eclipse-mosquitto
# build the MCZ Musa Maestro Python Controller image
docker-compose build
# run the container (detached)
docker-compose up -d
```

and stop it with

```bash
# stop the container
docker-compose down
```


## Examples

To send commands to the stove see:

- `examples/publish.py`: message pubblication examples;
- `musa/src/commands.py`: list of all known commands.

To retrieve the stove's infomation, see `examples/read.py`.

See also `musa/src/cfg.py` for the configuration parameters.

## Credits

[Chibald maestrogateway](https://github.com/Chibald/maestrogateway) and [Anthony-55 Maestro](https://github.com/Anthony-55/maestro)


## Diclaimer

**If** anyone will ever use this code, I do not take any responsability. Do not play with fire.


## License

This project is licensed under the WTFPL License.
