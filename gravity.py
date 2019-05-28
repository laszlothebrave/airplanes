from force import force
import numpy as np
import simulation
class GravityForce(force):
    def __init__(self):
        super().__init__([simulation.State.air])
    
    def calculate_force(self, piece):
        return np.array((0,0,-9.8 * piece.mass))