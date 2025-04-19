import spidev
import time

# Open SPI device (bus 1, device 0 = /dev/spidev1.0)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 8000000  # 8 MHz

def dotstar_send(r, g, b):
    # Sends start frame
    spi.writebytes([0x00, 0x00, 0x00, 0x00])
    
    # LED frame: 0b111xxxxx | B | G | R (note: order matters)
    brightness = 0xFF  # 0xE0 to 0xFF (higher = brighter)
    spi.writebytes([brightness, b, g, r])
    
    # End frame
    spi.writebytes([0xFF])

# Turn LED red
print("Lighting up red...")
dotstar_send(255, 0, 0)
time.sleep(2)

# Turn it off
print("Turning off...")
dotstar_send(0, 0, 0)

