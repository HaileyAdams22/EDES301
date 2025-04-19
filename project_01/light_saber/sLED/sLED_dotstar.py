from sLED_driver import DotStar # Import the DotStar class
import time
from sLED_driver2 import sLED  # Import the sLED class

strip = DotStar(num_leds=10, brightness=0.5)

try:
    strip.fill(255, 0, 0)  # All red
    time.sleep(1)

    strip.fill(0, 255, 0)  # All green
    time.sleep(1)

    strip.fill(0, 0, 255)  # All blue
    time.sleep(1)

    strip.clear()  # Turn off all LEDs
finally:
    strip.close()
