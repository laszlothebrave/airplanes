import numpy as np
from airplane import Airplane
from simulation import Simulation


plane = Airplane(100000, 1000)
plane.position = np.array((0., 0., 1000.))
plane.velocity = np.array((150., 50., 10.))
sim = Simulation(plane)

