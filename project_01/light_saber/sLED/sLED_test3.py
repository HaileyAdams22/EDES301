import sys
sys.path.append('/var/lib/cloud9/EDES301/project_01/light_saber')

from sLED_driver2 import sLED  # Import the sLED class
import time

if __name__ == '__main__':
    print("sLED Test")

    # Define your color values for x, y, and z
    x = 200  # Red value
    y = 0    # Green value
    z = 0    # Blue value
    color = (x, y, z)  # Create a tuple for the color (RGB)

    led = sLED(n_leds=60)  # Create an instance of the sLED class with 60 LEDs

    # Test single LED with color
    print("Lighting LED 0 with the color:", color)
    led.dotstar_send_single(0, *color)  # Send the color to the first LED
    time.sleep(2)  # Keep it on for 2 seconds

    # Test all LEDs with the same color
    print("Lighting all LEDs with the color:", color)
    colors = [color] * led.n_leds  # Create a list of the same color for all LEDs
    led.dotstar_send_all(colors)  # Send the color data to all LEDs
    time.sleep(2)  # Keep it on for 2 seconds

    # Turn off all LEDs
    print("Turning off all LEDs...")
    off_colors = [(0, 0, 0)] * led.n_leds  # Create a list of off colors for all LEDs
    led.dotstar_send_all(off_colors)  # Send the off color data to all LEDs
