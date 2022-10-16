# Rear Rider

## Project Overview

Rear Rider is an alert system to notify cyclists of approaching objects and vehicles from behind them. The system utilizes a rear mounted camera and radar. The radar will determine if an object is approaching the cyclist, while the camera will utilize some machine learning to identify the type of object that is approaching. The Rear Rider will leverage cellular data from the smartphone to delegate the object identification to a third party to minimize local processing power and maximize battery life. Users will receive a combination of audio and/or visual alerts through the companion app to be installed on their smartphone, with customizable sounds and visual cues for alerts. Additionally, users will be able to filter their alerts based on the approaching object (i.e. omit alerts for approaching cyclists).

## Team Members

- Jonathan Mendez
- Brock Morris
- Matthew O'Mara
- Bobby Palko
- Calin Pescaru
- Paul Sutton

## Creating a systemd service

The Bluetooth server needs to be up and running when the Raspberry Pi boots in order to have a seamless connection and experience. To achieve this goal a systemd service needs to be created.
In a text editor create a file, for example **rearrider.service**, and save it under **/etc/systemd/system**. Then, add the following lines:

	[Unit]
	Description=Bluetooth Server
	After=bluetooth.service

	[Service]
	ExecStart=/home/pi/path_to_server
	Restart=always

	[Install]
	WantedBy=bluetooth.target

Then, run these commands:

	sudo systemctl enable rearrider.service
	sudo systemctl daemon-reload

Now the Bluetooth server starts when the Pi boots. Also, Bluetooth has to be in discoverable mode so uncomment the line **DiscoverableTimeout = 0** under **/etc/bluetooth/main.conf**.
