## Install

```bash
sudo apt-get install hostapd
sudo apt-get install dnsmasq
```

# Configure Pi Static IP for wlan0

```bash
sudo nano /etc/dhcpcd.conf
# Add the following files to the end of the file
interface wlan0

static ip_address=192.168.5.10/24

denyinterfaces eth0
denyinterfaces wlan0
```

The IP address of the Pi will be 192.168.5.10 in the 192.168.5.xxx subnet.

# Configure IP address for iPhone

Go to wifi settings for the RearRider access point and set ipv4 address to manual 192.168.5.11 , or any number 11-15 (that is not the ip address of the pi).
Configure dns to manual and 192.168.5.10 (the ip address of the pi).

## Dnsmasq

```bash
sudo nano /etc/dnsmasq.d/dnsmasq.conf
# Add the following lines
interface=wlan0
dhcp-range=192.168.5.10,192.168.5.15,255.255.255.0,24h
```

## Hostap

```bash
sudo nano /etc/hostapd/hostapd.conf
# Add the following lines
interface=wlan0
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=NETWORK
wpa_passphrase=PASSWORD
```

Examples
- NETWORK: RearRiderPi4
- PASSWORD: make-a-strong-password

Then:

```bash
sudo nano /etc/default/hostapd
# Modify the following
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

## Traffic Forwarding

We do not need to setup traffic forwarding since we do not need the pi to forward any network requests. It would not make sense anyways since we only need network requests to and from the pi, not to the pi and out somewhere.

## IP Tables Rule (SKIP)
SKIP

## Finalize

```bash
sudo systemctl unmask hostapd.service
sudo systemctl enable hostapd.service
sudo systemctl enable dnsmasq.service
sudo rfkill unblock wlan
sudo reboot
```

Then run the `docs/picamera2_mjpeg_example.ipynb`

## Reference

https://www.instructables.com/Raspberry-Pi-Wifi-Hotspot/
