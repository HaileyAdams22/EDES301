# Import libraries
import spidev
import time
import random

#-----------------------------------------------------------------------
# DotStar
#-----------------------------------------------------------------------

"""
This code contains the final functions used in the DotStar class for the
light_saber project. It contains the following functions:

set_pixel_color : Sets the color of one pixel

clear : turns off all of sLED by setting colors to (0, 0, 0)

show : handles communication with sLED via SPI, with start_frame + tuple +
end_frame and uses a brightness multiplier

fill : sets all LEDs to the same color

close : cleanup function for dotstar -> closes SSPI connection

base_color : sets up base color of sLED

"""
class DotStar:
    
    def __init__(self, num_leds, brightness=1.0):
        self.num_leds = num_leds # number of LEDs on DotStar Strip
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
        
    def base_color():
        # Returns the baseline color as an RGB tuple
        return (255, 147, 41)  # Example baseline color (orange)