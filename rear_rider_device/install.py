#!/usr/bin/env bash
'''
This file does the following:
- Creates an executable bash file for the program.
  - TODO: Have the executable bash file detect if a virtual environment exists
    - If not:
      - create one following in the expected directory
      - edit .venv/pyenv.cfg to allow system site packages.
  - TODO: Have the executable bash file detect if the required python packages are downloaded
    - Download them if necessary
- Creates a systemd service file.
- Adds override to bluetooth service in order to disable some unused plugins.
- TODO: Modify other existing files to ensure proper Rear Rider device configuration.
  - dnsmasq, wifi
'''
import os
import subprocess
project_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    # This file should be in `rear_rider_device` so we need to travel up one
    # directories.
    f'{os.pardir}')
)
BLUETOOTH_OVERRIDE_DIR='/etc/systemd/system/bluetooth.service.d'
REAR_RIDER_SERVICE_FILE_NAME='rearrider.service'
SYSTEMD_SERVICES_DIR='/etc/systemd/system'
EXEC_FILE_LOCATION='/bin/rearrider'

print(f'Detected project path as {project_path}')

with open(EXEC_FILE_LOCATION, 'w', encoding='utf8') as exec_file:
    exec_file.write(
        '#!/bin/bash\n'
        f'source {project_path}/.venv/bin/activate\n'
        f'python {project_path}/rear_rider_device/main.py\n'
    )
chmod_res = subprocess.run(['chmod', '+x', EXEC_FILE_LOCATION])
chmod_res.check_returncode()
print(f'Created executable {EXEC_FILE_LOCATION}')

rear_rider_service_file=f'{SYSTEMD_SERVICES_DIR}/{REAR_RIDER_SERVICE_FILE_NAME}'
with open(rear_rider_service_file, 'w', encoding='utf8') as service_file:
    service_file.write(
        '[Unit]\n'
        'Description=Rear Rider\n'
        'After=bluetooth.service\n'

        '[Service]\n'
        'ExecStart=/bin/rearrider\n'
        'Restart=always\n'

        '[Install]\n'
        'WantedBy=bluetooth.target\n'
    )
print(f'Copied {rear_rider_service_file} -> {SYSTEMD_SERVICES_DIR}')

def create_bluetooth_override_dir():
    create_dir_res = subprocess.run(['mkdir', '-p', BLUETOOTH_OVERRIDE_DIR])
    create_dir_res.check_returncode()
create_bluetooth_override_dir()
with open(f'{BLUETOOTH_OVERRIDE_DIR}/override.conf', 'w', encoding='utf8') as bluetooth_override:
    bluetooth_override.write(
        '[Service]\n'
        # Clear the original value (yes we need to do this).
        'ExecStart=\n'
        # Assign a new value.
        'ExecStart=/usr/libexec/bluetooth/bluetoothd --noplugin=sap,avrcp\n'
    )


service_enable_res = subprocess.run(['systemctl', 'enable', REAR_RIDER_SERVICE_FILE_NAME])
service_enable_res.check_returncode()
print(f'Enable {SYSTEMD_SERVICES_DIR}/{REAR_RIDER_SERVICE_FILE_NAME}')

service_enable_res = subprocess.run(['systemctl', 'daemon-reload'])
service_enable_res.check_returncode()
print('Executed: systemctl daemon-reload')
