# Import board I/O pins
import board

# KMK core imports
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC

# KMK macro module (clean import)
from kmk.modules.macros import Macros, Press, Release, Tap

# Create keyboard instance
keyboard = KMKKeyboard()

# Load macro module
macros = Macros()
keyboard.modules.append(macros)

# Define input pins (order matters — match your physical wiring)
PINS = [board.D3, board.D4, board.D2, board.D1]

# Simple direct pin scanner (NOT a matrix)
keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# Keymap — cleaner, consistent style, and no weird KC.Macro vs KC.MACRO mixing
keyboard.keymap = [
    [
        KC.A,
        KC.DELETE,
        KC.MACRO("Hello world!"),
        KC.MACRO(Press(KC.LCMD), Tap(KC.S), Release(KC.LCMD)),  # CMD+S macro
    ]
]

# Run firmware
if __name__ == "__main__":
    keyboard.go()
