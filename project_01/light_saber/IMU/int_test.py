import smbus2
import time

# MPU6050 Registers and Constants
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
MOT_THR = 0x1F  # Motion detection threshold register
MOT_DUR = 0x20  # Motion detection duration register
INT_ENABLE = 0x38  # Interrupt enable register
INT_STATUS = 0x3A  # Interrupt status register
ACCEL_XOUT_H = 0x3B  # Accelerometer data register

# Initialize I2C bus
bus = smbus2.SMBus(2)

# Wake up MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# Function to configure motion detection
def configure_motion_detection():
    # Set motion detection threshold (0-255)
    motion_threshold = 0x10  # Set threshold for motion detection (higher values make the sensor less sensitive)
    bus.write_byte_data(MPU6050_ADDR, MOT_THR, motion_threshold)

    # Set motion detection duration (0-255, duration is in I2C clock cycles)
    motion_duration = 0x01  # Set the duration threshold
    bus.write_byte_data(MPU6050_ADDR, MOT_DUR, motion_duration)

    # Enable motion interrupt (bit 6 is for motion interrupt)
    bus.write_byte_data(MPU6050_ADDR, INT_ENABLE, 0x40)

    print("Motion detection configured.")

# Function to read the accelerometer data
def read_accel_data():
    high = bus.read_byte_data(MPU6050_ADDR, ACCEL_XOUT_H)
    low = bus.read_byte_data(MPU6050_ADDR, ACCEL_XOUT_H + 1)
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

# Function to check for motion interrupt
def check_motion_interrupt():
    interrupt_status = bus.read_byte_data(MPU6050_ADDR, INT_STATUS)
    # Check if the motion interrupt bit is set (bit 6)
    if interrupt_status & 0x40:
        return True
    return False
    
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

# Main function to initialize and detect motion
def main():
    # Configure motion detection
    configure_motion_detection()

    print("Waiting for motion detection...")
    try:
        while True:
            if check_motion_interrupt():
                print("Motion detected!")
                # Read accelerometer data (you could add more checks here, like if a certain threshold is passed)
                accel_x = read_accel_data()
                accel_y = read_accel_data()
                accel_z = read_accel_data()

                print(f"Accel (X, Y, Z): {accel_x}, {accel_y}, {accel_z}")

                # Clear interrupt (write 1 to clear interrupt in the register)
                bus.write_byte_data(MPU6050_ADDR, INT_STATUS, 0x40)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
