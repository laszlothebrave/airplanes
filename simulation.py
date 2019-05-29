from enum import Enum, auto

class State(Enum):
    initial = auto()
    air = auto()
    ground = auto()

import numpy as np

from airplane import Airplane
from piece import Piece
from wind import WindForce
from gravity import GravityForce


import numba


class Simulation:
    def __init__(self, plane, surface):
        self.state = 0
        self.plane = plane
        self.surface = surface
        self.forces = [WindForce(), GravityForce()]
        self.pieces = []
        
    @numba.jit()
    def step(self, dt):
        #update plane
        plane_forces = np.array((0.,0.,0.))
        for force in self.forces:
            plane_forces += force.get_force_vector(self.plane, self.state)
        print(plane_forces)
        if self.surface.is_below(self.plane.position):
            self.plane.velocity = np.array((0.,0.,0.))
            self.plane.state = 1
            plane_forces = np.array((0.,0.,0.))

        self.pieces += self.plane.step(plane_forces, dt)
            
        #update pieces
        for piece in self.pieces:
            if self.surface.is_below(piece.position):
                piece.state = 1
                continue
            piece_forces = np.array((0.,0.,0.))
            for force in self.forces:
                piece_forces += force.get_force_vector(piece, self.state)
                
            piece.step(piece_forces, dt)
        
        #single state :D
        self.state = 0  
            
    @numba.jit()
    def all_landed(self):
        b = self.surface.is_below(self.plane.position)
        for piece in self.pieces:
            b = b and self.surface.is_below(piece.position)
        return b
        