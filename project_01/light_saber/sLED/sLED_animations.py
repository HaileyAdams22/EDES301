from sLED_driver import DotStar
from sLED_test2.py import sLED  # Import the sLED class
import time

strip = DotStar(num_leds=10, brightness=1.0)

try:
    print("Fading blue...")
    strip.fade(color=(0, 0, 255), cycles=2)

    print("Flickering like a candle...")
    strip.flicker(base_color=(255, 147, 41), duration=5)

    print("Rainbow time!")
    strip.rainbow(wait_ms=10, iterations=2)

    strip.clear()

finally:
    strip.close()
