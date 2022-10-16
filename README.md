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

## Instructions on running the system

1. Make sure the Pi is up and running and that the OS is installed.
2. Clone the repo under /home/pi.
3. Follow the instructions under **Running main Rear Rider backend application** to install all the dependencies required.
4. Follow the instructions under **Create a systemd service**. This will create a service that starts automatically when Pi boots enabling the Bluetooth connection (as of right now create a service for the Bluetooth script under **rear_rider_device/rear_rider_bluetooth_server/src/main.py**).
5. Using Xcode, open the project under **Rear Rider** and install the application on your phone.
6. Reboot the Pi.
7. Now go to the iPhone's settings, Bluetooth, and connect to RearRiderPi4 once it's available.
8. Also, under the Wi-Fi settings, connect to the RearRider hotspot.
9. Now launch the Rear Rider app.

The application has three tabs. The first tab is the main view. Here the rider can see alerts when an object is approaching (TBD). The next view is the Live Streaming. The app will connect to the Pi over Wi-Fi and stream a live feed from the camera. The user has the option to record the streaming and to use ML to detect the objects in the feed. The last tab is the settings tab (TBD). At the top of the screen there are two icons that show if the Bluetooth and Wi-Fi connections are available by turning green.
