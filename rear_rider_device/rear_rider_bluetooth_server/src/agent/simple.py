#!/usr/bin/python
# SPDX-License-Identifier: LGPL-2.1-or-later

import dbus
import dbus.service

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

# bus = None
# device_obj = None
# dev_path = None

# def ask(prompt):
# 	try:
# 		return raw_input(prompt)
# 	except:
# 		return input(prompt)

# def set_trusted(path):
# 	props = dbus.Interface(bus.get_object("org.bluez", path),
# 					"org.freedesktop.DBus.Properties")
# 	props.Set("org.bluez.Device1", "Trusted", True)

# def dev_connect(path):
# 	dev = dbus.Interface(bus.get_object("org.bluez", path),
# 							"org.bluez.Device1")
# 	dev.Connect()

class Rejected(dbus.DBusException):
	_dbus_error_name = "org.bluez.Error.Rejected"

class Canceled(dbus.DBusException):
	_dbus_error_name = "org.bluez.Error.Canceled"

class Agent(dbus.service.Object):
	exit_on_release = True

	def set_exit_on_release(self, exit_on_release):
		self.exit_on_release = exit_on_release

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="", out_signature="")
	def Release(self):
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="os", out_signature="")
	def AuthorizeService(self, device, uuid):
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="s")
	def RequestPinCode(self, device):
		# Automatically approve pairing requests.
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="u")
	def RequestPasskey(self, device):
		pass


	@dbus.service.method(AGENT_INTERFACE,
					in_signature="ouq", out_signature="")
	def DisplayPasskey(self, device, passkey, entered):
		# Rear Rider device does not have a display.
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="os", out_signature="")
	def DisplayPinCode(self, device, pincode):
		# Rear Rider device does not have a display.
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="ou", out_signature="")
	def RequestConfirmation(self, device, passkey):
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="o", out_signature="")
	def RequestAuthorization(self, device):
		pass

	@dbus.service.method(AGENT_INTERFACE,
					in_signature="", out_signature="")
	def Cancel(self):
		pass