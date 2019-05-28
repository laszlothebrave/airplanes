from force import force
import numpy as np

class GravityForce(force):
    def __init__(self):
        super().__init__([0])
    
    def calculate_force(self, piece):
        return np.array((0,0,-9.8 * piece.mass))