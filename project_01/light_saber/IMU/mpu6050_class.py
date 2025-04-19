import smbus2
import time

class MPU6050:
    def __init__(self, bus_num=2, address=0x68):
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        self.PWR_MGMT_1 = 0x6B
        self.init_sensor()

    def init_sensor(self):
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0)

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def get_sensor_data(self):
        data = {
            "accel_x": (self.read_raw_data(0x3B) / 16384.0) - 0.1,
            "accel_y": (self.read_raw_data(0x3D) / 16384.0) + 0.03,
            "accel_z": (self.read_raw_data(0x3F) / 16384.0) + 0.16,
            "gyro_x": (self.read_raw_data(0x43) / 131.0) + 2.3,
            "gyro_y": (self.read_raw_data(0x45) / 131.0) - 0.6,
            "gyro_z": (self.read_raw_data(0x47) / 131.0) + 0.78,
        }

        data["tot_accel"] = data["accel_x"] + data["accel_y"] + data["accel_z"] - 1
        data["tot_gyro"] = data["gyro_x"] + data["gyro_y"] + data["gyro_z"]
        data["comb_accel_gyro"] = abs(data["tot_accel"]) + abs(data["tot_gyro"] / 100)
        return data
