import time
import sys
import threading

# Add the path to your LED and ThreadedButton classes if needed
# sys.path.append("/path/to/your/modules")

from led import LED
from threaded_button import ThreadedButton
from sLED_DotStar import DotStar
from sLED_Animations import Animations

# Pin assignments
led_pins = ["P2_2", "P2_4", "P2_6", "P2_8"]
button_pin = "P2_19"  # Button 1

# Initialize mLEDs
leds = [LED(pin) for pin in led_pins]
current_index = [0]  # Use list for mutability inside nested function
first_press = [True]  # Mutable so we can change it inside the callback

# Initialize sLED
sLED = DotStar(num_leds=30, brightness=0.8)  # Adjust LED count & brightness
sLED.clear()
led_colors = [
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (255, 255, 255) # White
]

# Turn off all LEDs
for led in leds:
    led.off()

# Flag to track if sLED is active (on)
sLED_active = False

# Initialize animations
animations = Animations(sLED)

def handle_button_release():
    global sLED_active  # Make sure we update the global variable

    press_duration = button.get_last_press_duration()

    if press_duration >= 2.0:  # Long press (2 seconds or more)
        print("Long press detected!")

        if sLED_active:  # If sLED is already on, turn it off with animation
            print("Turning off sLED...")
            animations.light_down(base_color=lambda: led_colors[current_index[0]], speed=0.1)
            sLED_active = False  # Mark sLED as inactive
        else:  # If sLED is off, turn it on with animation and match mLED color
            print("Activating sLED...")
            r, g, b = led_colors[current_index[0]]
            animations.light_up(base_color=lambda: (r, g, b), speed=0.1)
            sLED_active = True  # Mark sLED as active

        # Keep the current mLED on
        leds[current_index[0]].on()
    else:  # Short press (less than 2 seconds)
        print(f"Short press ({press_duration:.2f}s) - cycling mLED")

        # Cycle mLEDs
        if first_press[0]:  # First press logic
            leds[current_index[0]].on()
            first_press[0] = False
        else:
            leds[current_index[0]].off()  # Turn off the current mLED
            current_index[0] = (current_index[0] + 1) % len(leds)  # Move to next LED
            leds[current_index[0]].on()  # Turn on the next mLED

        # Update sLED only if it is active
        if sLED_active:
            r, g, b = led_colors[current_index[0]]
            sLED.fill(r, g, b)

# Initialize the button
button = ThreadedButton(pin=button_pin, sleep_time=0.05)

# Only use on_release_callback now (no press logic needed)
button.set_on_release_callback(handle_button_release)

# Start the button thread
button.start()

print("Press Button 1 to cycle through LEDs. Press Ctrl-C to exit.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    button.cleanup()
    for led in leds:
        led.cleanup()
    sLED.clear()
    sLED.close()
