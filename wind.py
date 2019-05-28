from force import force
import numpy as np

import matplotlib.pyplot as plt

def x_from_pressure(pressure):
    return (pressure[:,:-2] - pressure[:,2:])[1:-1]

def y_from_pressure(pressure):
    return (pressure[2:, :] - pressure[:-2, :])[:, 1:-1]

def generate_pressure():
    return 1000 + np.random.exponential(5, size=(2200,2200))

class WindForce(force):
    def __init__(self):
        super().__init__([0])
        self.pressure = generate_pressure()
        self.x_velocity = x_from_pressure(self.pressure)
        self.y_velocity = y_from_pressure(self.pressure)

    def calculate_force(self, piece):
        return piece.air_friction_factor * (self.get_wind(*piece.position) - piece.velocity)
        
    def get_wind(self, x, y, z):        
        indices = np.array((x/100 + 100, y/100 + 100, z/100 + 100))
        rounded = np.round(indices).astype(np.int)
        
        center_weights = 1 - np.abs(rounded - indices)
        sign = np.sign(indices - rounded).astype(np.int)
        
        x_1 = self.x_velocity[rounded[0], rounded[1]]
        x_2 = self.x_velocity[rounded[0] + sign[0], rounded[1]]
        
        y_1 = self.y_velocity[rounded[0], rounded[1]]
        y_2 = self.y_velocity[rounded[0], rounded[1] + sign[1]]
        
        wind_x = x_1 * center_weights[0] + x_2 * (1-center_weights[0]) #linear interpolation
        wind_y = y_1 * center_weights[1] + y_2 * (1-center_weights[1])

        return np.array((wind_x, wind_y, 0))

if __name__ == "__main__":
    a = WindForce()
    zzz = a.get_wind(501,0,0)
    plt.contourf(a.pressure)