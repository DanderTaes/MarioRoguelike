""" XInput Game Controller APIs
Pure Python implementation for reading Xbox controller inputs without extra libs
Copyright (C) 2020 by Arti Zirk <arti.zirk@gmail.com>
Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted.
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
"""

from ctypes import WinDLL, WinError, Structure, POINTER, byref, c_ubyte
from ctypes.util import find_library
from ctypes.wintypes import DWORD, WORD, SHORT
from keyboard import press, release

# for some reason wintypes.BYTE is defined as signed c_byte and as c_ubyte
BYTE = c_ubyte

class XINPUT_BUTTONS(Structure):
	"""Bit-fields of XINPUT_GAMEPAD wButtons"""

	_fields_ = [
		("DPAD_UP", WORD, 1),
		("DPAD_DOWN", WORD, 1),
		("DPAD_LEFT", WORD, 1),
		("DPAD_RIGHT", WORD, 1),
		("START", WORD, 1),
		("BACK", WORD, 1),
		("LEFT_THUMB", WORD, 1),
		("RIGHT_THUMB", WORD, 1),
		("LEFT_SHOULDER", WORD, 1),
		("RIGHT_SHOULDER", WORD, 1),
		("_reserved_1_", WORD, 1),
		("_reserved_1_", WORD, 1),
		("A", WORD, 1),
		("B", WORD, 1),
		("X", WORD, 1),
		("Y", WORD, 1)
	]
	
	def __repr__(self):
		r = []
		for name, type, size in self._fields_:
			if "reserved" in name:
				continue
			r.append("{}={}".format(name, getattr(self, name)))
		args = ', '.join(r)
		return f"XINPUT_GAMEPAD({args})"
	

class XINPUT_GAMEPAD(Structure):
	"""Describes the current state of the Xbox 360 Controller.
	
	https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_gamepad
	
	wButtons is a bitfield describing currently pressed buttons
	"""
	_fields_ = [
		("wButtons", XINPUT_BUTTONS),
		("bLeftTrigger", BYTE),
		("bRightTrigger", BYTE),
		("sThumbLX", SHORT),
		("sThumbLY", SHORT),
		("sThumbRX", SHORT),
		("sThumbRY", SHORT),
	]
	
	def __repr__(self):
		r = []
		for name, type in self._fields_:
			r.append("{}={}".format(name, getattr(self, name)))
		args = ', '.join(r)
		return f"XINPUT_GAMEPAD({args})"


class XINPUT_STATE(Structure):
	"""Represents the state of a controller.
	
	https://docs.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_state
	
	dwPacketNumber: State packet number. The packet number indicates whether
		there have been any changes in the state of the controller. If the
		dwPacketNumber member is the same in sequentially returned XINPUT_STATE
		structures, the controller state has not changed.
	"""
	_fields_ = [
		("dwPacketNumber", DWORD),
		("Gamepad", XINPUT_GAMEPAD)
	]
	
	def __repr__(self):
		return f"XINPUT_STATE(dwPacketNumber={self.dwPacketNumber}, Gamepad={self.Gamepad})"

class XInput:
	"""Minimal XInput API wrapper"""

	def __init__(self):
		# https://docs.microsoft.com/en-us/windows/win32/xinput/xinput-versions
		# XInput 1.4 is available only on Windows 8+.
		# Older Windows versions are End Of Life anyway.
		self.pressed_keys = set()
		self.prev_button_state = None
		lib_name = "XInput1_4.dll"  
		lib_path = find_library(lib_name)
		if not lib_path:
			raise Exception(f"Couldn't find {lib_name}")
		self._XInput_ = WinDLL(lib_path)
		self._XInput_.XInputGetState.argtypes = [DWORD, POINTER(XINPUT_STATE)]
		self._XInput_.XInputGetState.restype = DWORD

	def GetState(self, dwUserIndex):
		state = XINPUT_STATE()
		ret = self._XInput_.XInputGetState(dwUserIndex, byref(state))
		if ret:
			raise WinError(ret)
		return state.dwPacketNumber, state.Gamepad

	def run(self):
		packet_number, gamepad_state = self.GetState(0)
		self.simulate_keyboard_input(gamepad_state.wButtons)

	"""
	Añadido simulate_keyboard_input por Ander Gaytán para tomar inputs de un mando y simular una presion del teclado cada frame del juego
	"""

	def simulate_keyboard_input(self, button_state):
        # Simulate keyboard inputs based on the controller button state
		self.release_previous_keys()

		if button_state.DPAD_UP:
			press('w')
			self.pressed_keys.add('w')

		if button_state.DPAD_DOWN:
			press('s')
			self.pressed_keys.add('s')

		if button_state.DPAD_LEFT:
			press('a')
			self.pressed_keys.add('a')

		if button_state.DPAD_RIGHT:
			press('d')
			self.pressed_keys.add('d')

		if button_state.A:
			press("space")
			self.pressed_keys.add("space")

	def release_previous_keys(self):
		# Release keys that were pressed in the previous frame but not in the current frame
		for key in self.pressed_keys.copy():
			release(key)
			self.pressed_keys.remove(key)
		

