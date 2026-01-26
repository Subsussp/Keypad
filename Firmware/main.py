import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# HID devices
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# ===== Switches =====
switch_pins = [board.RX, board.SCL, board.TX, board.MISO, board.MOSI]
switches = []

for pin in switch_pins:
    sw = digitalio.DigitalInOut(pin)
    sw.direction = digitalio.Direction.INPUT
    sw.pull = digitalio.Pull.UP
    switches.append(sw)

# ===== Rotary encoder =====
enc_a = digitalio.DigitalInOut(board.A2)
enc_a.direction = digitalio.Direction.INPUT
enc_a.pull = digitalio.Pull.UP

enc_b = digitalio.DigitalInOut(board.A1)
enc_b.direction = digitalio.Direction.INPUT
enc_b.pull = digitalio.Pull.UP

last_state = (enc_a.value << 1) | enc_b.value

print("Macropad started. Press switches or rotate encoder...")

while True:
    # --- Check switches ---
    for i, sw in enumerate(switches):
        if not sw.value:  # pressed
            print(f"Switch {i} pressed")
            if i == 0:
                # Button 0 opens Chrome (Windows)
                # Win + R
                kbd.press(Keycode.WINDOWS)
                kbd.press(Keycode.R)
                kbd.release_all()
                time.sleep(0.1)
                # Type "chrome"
                for c in "chrome":
                    kbd.press(getattr(Keycode, c.upper()))
                    kbd.release_all()
                # Press Enter
                kbd.press(Keycode.ENTER)
                kbd.release_all()
            else:
                # Other buttons send letters A-E
                kbd.press(Keycode.A + i)
                kbd.release_all()
            time.sleep(0.2)  # debounce

    # --- Check encoder (volume) ---
    current_state = (enc_a.value << 1) | enc_b.value
    if current_state != last_state:
        # simple quadrature logic
        if last_state == 0b00:
            if current_state == 0b01:
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                print("Volume Up")
            elif current_state == 0b10:
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                print("Volume Down")
        elif last_state == 0b01:
            if current_state == 0b11:
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                print("Volume Up")
            elif current_state == 0b00:
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                print("Volume Down")
        elif last_state == 0b11:
            if current_state == 0b10:
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                print("Volume Up")
            elif current_state == 0b01:
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                print("Volume Down")
        elif last_state == 0b10:
            if current_state == 0b00:
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                print("Volume Up")
            elif current_state == 0b11:
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                print("Volume Down")

        last_state = current_state
        time.sleep(0.002)  # tiny debounce
