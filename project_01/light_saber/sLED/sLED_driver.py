""" sLED Driver """

import spidev
import time
import random
from sLED_test2.py import sLED  # Import the sLED class

class DotStar:
    def __init__(self, num_leds, brightness=1.0):
        self.num_leds = num_leds
        self.brightness = max(0.0, min(brightness, 1.0))  # Clamp between 0.0 and 1.0
        self.pixels = [(0, 0, 0)] * num_leds  # RGB tuples

        # Initialize SPI1 on PocketBeagle
        self.spi = spidev.SpiDev()
        self.spi.open(1, 0)  # bus 1, device 0 = SPI1 on PocketBeagle
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

    def rainbow(self, wait_ms=20, iterations=1):
        for j in range(256 * iterations):
            for i in range(self.num_leds):
                pixel_index = (i * 256 // self.num_leds + j) & 255
                self.set_pixel_color(i, *self.wheel(pixel_index))
            self.show()
            time.sleep(wait_ms / 1000.0)

    def flicker(self, base_color=(255, 147, 41), flicker_range=30, duration=5.0, speed=0.05):
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