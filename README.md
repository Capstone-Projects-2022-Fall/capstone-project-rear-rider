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


## Running main Rear Rider backend application.

```bash
sudo apt-get install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev python3-venv gir1.2-gtk-3.0 libglib2.0-dev
# Create a virtual environment in python if not done so yet.
python -m venv .venv

# Edit .venv/pyenv.cfg to allow the virtual environment access to python packages downloaded from `apt-get install`.
# Add the following line to the aforementioned file:
# include-system-site-packages = true

# Activate the virtual environment.
source .venv/bin/activate
# Install the required python packages from pip.
pip install -r ./requirements.txt
# Change the working directory to the rear rider device directory.
cd ./rear_rider_device
python ./main.py
```

