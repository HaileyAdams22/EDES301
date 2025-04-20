# Import libraries
import spidev
import time
import random
from sLED_DotStar import DotStar


#-----------------------------------------------------------------------
# sLED
#-----------------------------------------------------------------------

""" 
This code contains the final functions used in the sLED class for the 
light_saber project. It contains the following functions:

light_up : animates the sLED to light up from base - UNFINISHED

flicker : flickers sLED around a base color while movement is occuring 
detected by MPU.

flash : flash sLED around a base color when the MPU detects a major 
acceleration change occurs using the interrupt pin.

light_down : animates sLED to turn off from end - UNFINISHED

"""

class Animations:
    
    def __init__(self, led_strip):
        self.led_strip = led_strip
        self.num_leds = led_strip.num_leds

    # Delegate LED functions to DotStar instance
    def set_pixel_color(self, n, r, g, b):
        self.led_strip.set_pixel_color(n, r, g, b)

    def show(self):
        self.led_strip.show()

    def fill(self, r, g, b):
        self.led_strip.fill(r, g, b)
    
    def light_up(self, base_color=lambda: (255, 147, 41), speed=0.1):
        
        
        """
        Lights up the LEDs starting from both the first and last LED and meeting at the middle.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple for the baseline color.
        - speed: The speed of the animation (delay between each step).
        """
        r_base, g_base, b_base = base_color()

        # Set up two pointers: one starting at the first LED and one at the last LED
        start = 0
        end = self.num_leds - 1

        # Continue lighting up LEDs until the two pointers meet in the middle
        while start <= end:
            # Turn on LEDs at both the start and end pointers
            self.set_pixel_color(start, r_base, g_base, b_base)
            self.set_pixel_color(end, r_base, g_base, b_base)
           
            # Update the LEDs and move towards the center
            self.show()
            time.sleep(speed)

            # Move the pointers towards the center
            start += 1
            end -= 1

    
    
    def flicker(self, base_color=lambda: (255, 147, 41), flicker_range=30, speed=0.05, is_active_func=lambda: False):
        """
        Flickers LEDs around a base color while `is_active_func()` is True.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple.
        - flicker_range: Int, range of flicker variation.
        - speed: Float, delay between updates.
        - is_active_func: Function that returns True if flickering should continue.
        """
        while is_active_func():
            r_base, g_base, b_base = base_color()
            for i in range(self.num_leds):
                r = max(0, min(255, r_base + random.randint(-flicker_range, flicker_range)))
                g = max(0, min(255, g_base + random.randint(-flicker_range, flicker_range)))
                b = max(0, min(255, b_base + random.randint(-flicker_range, flicker_range)))
                self.set_pixel_color(i, r, g, b)
            self.show()
            time.sleep(speed)
        
    
    def flash(self, base_color=lambda: (255, 147, 41), flash_duration=0.1, flash_speed=0.05):
        """
        Turns the LEDs from baseline color to a very quick and bright flash of white, 
        then returns to the original baseline color.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple for the baseline color.
        - flash_duration: Time (in seconds) the flash of white will last.
        - flash_speed: Speed at which to perform the transition (controls delay between updates).
        """
    
        # Save the original base color
        r_base, g_base, b_base = base_color()
    
        # Step 1: Set all LEDs to baseline color
        self.fill(r_base, g_base, b_base)
    
        # Step 2: Flash to white (very quick)
        self.fill(255, 255, 255)  # Full white color flash
        time.sleep(flash_duration)  # Duration of the flash
     
        # Step 3: Return to the original baseline color
        self.fill(r_base, g_base, b_base)

    
    def light_down(self, base_color=lambda: (255, 147, 41), speed=0.1):
        """
        Powers down the LEDs starting from the middle LED and turning off LEDs towards both ends.
    
        Parameters:
        - base_color_func: Function that returns an (R, G, B) tuple for the baseline color.
        - speed: The speed of the animation (delay between each step).
        """
        r_base, g_base, b_base = base_color()

        # Set up pointer starting from the middle LED
        middle = self.num_leds // 2  # Always works for odd numbers

        # Continue powering down LEDs until we reach the ends of the strip
        for i in range(middle + 1):
            # Turn off LEDs at positions moving outwards from the middle
            self.set_pixel_color(middle - i, 0, 0, 0)  # Turning off from the middle left
            self.set_pixel_color(middle + i, 0, 0, 0)  # Turning off from the middle right

            # Update the LEDs and pause before the next step
            self.show()
            time.sleep(speed)
