""" This code checks for connection of the pocket beagle to the IMU. """

import smbus2

MPU6050_ADDR = 0x68  # Default I2C address
WHO_AM_I = 0x75      # WHO_AM_I register address

try:
    bus = smbus2.SMBus(2)  # I2C bus 2
    who_am_i = bus.read_byte_data(MPU6050_ADDR, WHO_AM_I)
    print(f"WHO_AM_I register: {hex(who_am_i)}")
except OSError as e:
    print(f"I2C Error: {e}")


try:
    bus = smbus2.SMBus(2)  # I2C bus 2
    data = bus.read_byte_data(0x68, 0x75)  # Try to read WHO_AM_I register
    print(f"Response from device: {data}")
except OSError as e:
    print(f"I2C Error: {e}")

