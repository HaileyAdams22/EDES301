""" sLED Driver """

import spidev
import time
import random
from sLED_driver2 import sLED2  # Import the sLED class

class DotStar:
    def __init__(self, num_leds, brightness=1.0):
        self.num_leds = num_leds
        self.brightness = max(0.0, min(brightness, 1.0))  # Clamp between 0.0 and 1.0
        self.pixels = [(0, 0, 0)] * num_leds  # RGB tuples

        # Initialize SPI1 on PocketBeagle
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # bus 1, device 0 = SPI1 on PocketBeagle
        self.spi.max_speed_hz = 4000000  # 4 MHz is a safe speed
        self.spi.mode = 0b00

    def set_pixel_color(self, n, r, g, b):
        if 0 <= n < self.num_leds:
            self.pixels[n] = (r, g, b)

    def clear(self):
        self.pixels = [(0, 0, 0)] * self.num_leds
        self.show()

    def show(self):
        start_frame = [0x00] * 4
        end_frame = [0xFF] * ((self.num_leds + 15) // 16)

        led_data = []
        for r, g, b in self.pixels:
            r = int(r * self.brightness)
            g = int(g * self.brightness)
            b = int(b * self.brightness)
            led_data.extend([0xFF, b, g, r])  # DotStar expects BGR + header

        self.spi.xfer2(start_frame + led_data + end_frame)

    def fill(self, r, g, b):
        for i in range(self.num_leds):
            self.set_pixel_color(i, r, g, b)
        self.show()

    def close(self):
        self.spi.close()
        
        
    """
    wheel(self, pos): This function generates a smooth 
    transition of rainbow colors based on the position (pos), 
    which is an integer between 0 and 255.
    """

    def wheel(self, pos):
        """Color wheel helper to get rainbow colors."""
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return (pos * 3, 0, 255 - pos * 3)


    """ 
    rainbow(self, wait_ms=20, iterations=1): 
    This method creates a rainbow animation that runs for 
    iterations cycles, with each cycle containing 256 positions.
    """
    
    def rainbow(self, wait_ms=20, iterations=1):
        for j in range(256 * iterations):
            for i in range(self.num_leds):
                pixel_index = (i * 256 // self.num_leds + j) & 255
                self.set_pixel_color(i, *self.wheel(pixel_index))
            self.show()
            time.sleep(wait_ms / 1000.0)
            
    """
    flicker(self, base_color=(255, 147, 41), flicker_range=30, duration=5.0, 
    speed=0.05): This method creates a flicker effect where the 
    LEDs randomly change colors within a specified range (flicker_range) 
    around a base color (base_color).
    
    'duration' controls how long the flicker lasts
    'speed' controls how fast the flickering happens
    """

    def flicker2(self, base_color=(255, 147, 41), flicker_range=30, duration=5.0, speed=0.05):
        end_time = time.time() + duration
        r_base, g_base, b_base = base_color
        while time.time() < end_time:
            for i in range(self.num_leds):
                r = max(0, min(255, r_base + random.randint(-flicker_range, flicker_range)))
                g = max(0, min(255, g_base + random.randint(-flicker_range, flicker_range)))
                b = max(0, min(255, b_base + random.randint(-flicker_range, flicker_range)))
                self.set_pixel_color(i, r, g, b)
            self.show()
            time.sleep(speed)
            
    """
    fade(self, color=(0, 0, 255), steps=50, cycles=3, delay=0.02): 
    This method creates a fade-in and fade-out effect for a given color (color).
    
    'steps' controls how smooth the fade is
    'cycles' controls how many times the fade effect repeats
    'delay' controls the speed of the fade
    """
            
    def fade(self, color=(0, 0, 255), steps=50, cycles=3, delay=0.02):
        r, g, b = color
        for _ in range(cycles):
            # Fade in
            for i in range(steps):
                brightness = i / steps
                for j in range(self.num_leds):
                    self.set_pixel_color(j, int(r * brightness), int(g * brightness), int(b * brightness))
                self.show()
                time.sleep(delay)
            # Fade out
            for i in range(steps, -1, -1):
                brightness = i / steps
                for j in range(self.num_leds):
                    self.set_pixel_color(j, int(r * brightness), int(g * brightness), int(b * brightness))
                self.show()
                time.sleep(delay)
                
              
                
        """
        Flickers between full brightness and a dimmer flickered version of the same color.
        Doesn't go fully dark during pauses.
        """
                
                
    def unstable_flicker(self, base_color=(0, 0, 255), flicker_range=0.5, duration=10.0, dim_idle=0.2):
            
        start_time = time.time()
        r_base, g_base, b_base = base_color

        while time.time() - start_time < duration:
            # Flicker burst
            burst_duration = random.uniform(0.2, 0.6)
            burst_end = time.time() + burst_duration
            while time.time() < burst_end:
                flicker_factor = random.uniform(1.0 - flicker_range, 1.0)
                for i in range(self.num_leds):
                    r = int(r_base * flicker_factor)
                    g = int(g_base * flicker_factor)
                    b = int(b_base * flicker_factor)
                    self.set_pixel_color(i, r, g, b)
                self.show()
                time.sleep(random.uniform(0.01, 0.05))  # Very fast flicker rate

            # Dim idle glow (instead of turning off)
            for i in range(self.num_leds):
                self.set_pixel_color(i, int(r_base * dim_idle), int(g_base * dim_idle), int(b_base * dim_idle))
            self.show()
            time.sleep(random.uniform(0.5, 2.0))  # Pause before next flicker burst
