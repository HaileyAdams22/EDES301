from sLED_driver import DotStar
from sLED_driver2 import sLED2  # Import the sLED class
import time

strip = DotStar(num_leds=30, brightness=1.0)

try:
    print("Fading blue...")
    strip.fade(color=(0, 0, 255), cycles=2)

    print("Flickering like a candle...")
    strip.flicker2(base_color=(0, 0, 255), duration=5)

    print("Rainbow time!")
    strip.rainbow(wait_ms=10, iterations=2)
    
    print("Dim Flicker...")
    strip.unstable_flicker(base_color=(0, 0, 255), flicker_range=0.5, duration=10.0, dim_idle=0.2)

    strip.clear()

finally:
    strip.close()
