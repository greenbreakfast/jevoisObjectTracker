# jevoisObjectTracker
Program to configure the JeVois Computer Vision machine

## TODO:

* ~~colourConv~~
	* ~~convert (360deg, 1.0, 1.0) HSV val to values out of 255~~
* mqtt
	* ~~implement listening to an mqtt server to program jevois with color val~~
	* **NEEDS TESTING**

## Operation



* `python objectTracker.py`
	* Programs Jevois to track colour from command line argument
* `python mqttObjectTracker.py`
	* Listens to MQTT `color` topic for HSV color values, then programs the Jevois to track that color.


## Running on the Omega2

This can be run on the Onion Omega2

### Installation

```
opkg update
opkg install python-light python-pyserial python-pip
```

```
pip install --upgrade setuptools
pip install paho-mqtt
```