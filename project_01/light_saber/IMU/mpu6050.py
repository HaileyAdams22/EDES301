import smbus2
import time

# MPU6050 Registers and Addresses
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48

# Initialize I2C bus
bus = smbus2.SMBus(2)  # Use I2C bus 2, corresponding to P1_28 and P1_26 on PocketBeagle

# Initialize MPU6050
def init_mpu6050():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Wake up MPU6050

# Read raw data from two bytes and convert to signed integer
def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value -= 65536
    return value

# Fetch and display accelerometer and gyroscope data
def get_sensor_data():
    # Read accelerometer data
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)

    # Read gyroscope data
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    # Convert raw data to "g" and degrees per second
    accel_x_scaled = (accel_x / 16384.0) - 0.1  # Scale for accelerometer
    accel_y_scaled = (accel_y / 16384.0) + 0.03
    accel_z_scaled = (accel_z / 16384.0) + 0.16

    gyro_x_scaled = (gyro_x / 131.0) + 2.3  # Scale for gyroscope
    gyro_y_scaled = (gyro_y / 131.0) - 0.6
    gyro_z_scaled = (gyro_z / 131.0) + 0.78
    
    tot_accel = accel_x_scaled + accel_y_scaled + accel_z_scaled - 1
    tot_gyro = gyro_x_scaled + gyro_y_scaled + gyro_z_scaled 
    comb_accel_gyro = abs(tot_accel) + abs(tot_gyro/100)

    return {
        "accel_x": accel_x_scaled,
        "accel_y": accel_y_scaled,
        "accel_z": accel_z_scaled,
        "gyro_x": gyro_x_scaled,
        "gyro_y": gyro_y_scaled,
        "gyro_z": gyro_z_scaled,
        "tot_accel": tot_accel,
        "tot_gyro": tot_gyro,
        "comb_accel_gyro": comb_accel_gyro,
    }

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

# Main function to fetch and display sensor data at 60Hz
def main():
    init_mpu6050()
    print("MPU6050 Initialized. Reading data at 60Hz...\n")
    try:
        while True:
            data = get_sensor_data()
            print(
                f"Accel (g): X={data['accel_x']:.2f}, Y={data['accel_y']:.2f}, Z={data['accel_z']:.2f} | "
                f"Gyro (°/s): X={data['gyro_x']:.2f}, Y={data['gyro_y']:.2f}, Z={data['gyro_z']:.2f} | "
                f"Totals: Acceleration={data['tot_accel']:.2f}, Gyro={data['tot_gyro']:.2f}, Combined={data['comb_accel_gyro']:.2f}"
            )
            time.sleep(1 / 60.0)  # 1 Read per second currently
    except KeyboardInterrupt:
        print("\nExiting program.")

if __name__ == "__main__":
    main()
