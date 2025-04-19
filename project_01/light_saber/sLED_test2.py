import spidev
import time
import random  # Import the random module

class sLED:

    def __init__(self, n_leds=60):
        # Open SPI device (bus 1, device 0 = /dev/spidev1.0)
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 8000000  # 8 MHz
        self.n_leds = n_leds  # Set the number of LEDs on the strip
        self.end_frame_bytes = [0xFF]


    def dotstar_send_single(self, led_num, r, g, b):
        """Sends color data to a single LED in the strip"""
        if led_num < 0 or led_num >= self.n_leds:
            print(f"LED number {led_num} is out of range")
            return

        # Start frame
        self.spi.writebytes([0x00, 0x00, 0x00, 0x00])
        
        # Send color data for the specified LED
        brightness = 0xE5  # 0xE0 to 0xFF (higher = brighter)
        self.spi.writebytes([brightness, b, g, r])  # Note: BGR order
        
        # Fill the remaining LEDs with off color
        for _ in range(self.n_leds - 1):
            self.spi.writebytes([0x00, 0x00, 0x00, 0x00])  # Off

        # End frame
        self.spi.writebytes(self.end_frame_bytes)


    def dotstar_send_all(self, led_colors):
        """Sends color data to all LEDs in the strip"""
        if len(led_colors) != self.n_leds:
            print(f"Error: Expected {self.n_leds} LEDs, but got {len(led_colors)}")
            return

        # Start frame
        self.spi.writebytes([0x00, 0x00, 0x00, 0x00])
    
        # Send color data for each LED in the strip
        for r, g, b in led_colors:
            brightness = 0xE5  # 0xE0 to 0xFF (higher = brighter)
            self.spi.writebytes([brightness, b, g, r])  # Note: BGR order
    
        # End frame
        self.spi.writebytes(self.end_frame_bytes)

    def random_color(self):
        """Generate a random color between 0 and 192"""
        return random.randrange(0, 7) * 32


    def generate_random_colors(self):
        """Generate random colors for all LEDs"""
        led_colors = []
        for _ in range(self.n_leds):
            r = self.random_color()
            g = self.random_color()
            b = self.random_color()
            led_colors.append((r, g, b))  # Append the color for this LED
        return led_colors
        
        
    def clear_strip(self):
        """Turns off all LEDs on the strip"""
        off_colors = [(0, 0, 0)] * self.n_leds
        self.dotstar_send_all(off_colors)

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("sLED Test")
    
    led = sLED(n_leds=60)  # Create an instance of the sLED class with 30 LEDs
    single_led = 1

    # Turn off at the beginning
    print("Beginning Test")
    off_colors = [(0, 0, 0)] * led.n_leds
    led.dotstar_send_all(off_colors)
    
    
    
    # Turn single LED on as red
    print("Single LED Red")
    single_led_color = (255, 0, 0)
    led.dotstar_send_single(single_led, *single_led_color)  # Light up the first LED with a random color
    time.sleep(2)
    
    # Test Random Function for a single LED
    print("Single LED Random")
    single_led_color = (led.random_color(), led.random_color(), led.random_color())
    led.dotstar_send_single(single_led, *single_led_color)  # Light up the first LED with a random color
    time.sleep(2)
    
    
    
    # Turn all LEDs red
    print("Lighting up all LEDs red...")
    red_colors = [(255, 0, 0)] * led.n_leds  # Create a list of red colors for all LEDs
    led.dotstar_send_all(red_colors)  # Send the red color data to the LEDs
    time.sleep(2)

    # Turn all LEDs off
    print("Turning off all LEDs...")
    off_colors = [(0, 0, 0)] * led.n_leds  # Create a list of off colors for all LEDs
    led.dotstar_send_all(off_colors)  # Send the off color data to the LEDs
    time.sleep(2)



    # Test Random Function for all LEDs
    print("Lighting up all LEDs with random colors...")
    random_colors = led.generate_random_colors()
    led.dotstar_send_all(random_colors)
    time.sleep(2)

    # Turn off at the end
    print("Turning off all LEDs...")
    off_colors = [(0, 0, 0)] * led.n_leds
    led.dotstar_send_all(off_colors)
    
    
    
    # Light up one LED at a time
    led.clear_strip()
    time.sleep(0.5)
    for i in range(led.n_leds):
        print(f"Lighting LED {i}")
        frame = [(0, 0, 0)] * led.n_leds
        frame[i] = (255, 255, 255)
        led.dotstar_send_all(frame)
        time.sleep(0.25)
        
    # Turn everything off again
    print("Turning off all LEDs...")
    led.clear_strip()
    time.sleep(1)
