import board
import busio as io
import adafruit_mlx90614

from time import sleep


class TemperatureSensor:
    def __init__(self):
        self.i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
        self.mlx = adafruit_mlx90614.MLX90614(self.i2c)
    
    def get_target_temperature(self):
        return "{:.2f}".format(self.mlx.object_temperature)
    
    def get_ambient_temperature(self):
        return "{:.2f}".format(mlx.ambient_temperature) 

