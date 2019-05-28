import numpy as np

from airplane import Airplane
from piece import Piece
from wind import WindForce
from gravity import GravityForce

from enum import Enum, auto

class State(Enum):
    initial = auto()
    air = auto()
    ground = auto()

class Simulation:
    def __init__(self, plane):
        self.state = State.initial
        self.plane = plane
        self.forces = [WindForce(), GravityForce()]
        self.pieces = []
        
    def step(self, dt):
        #update plane
        plane_forces = np.array((0.,0.,0.))
        for force in self.forces:
            plane_forces += force.get_force_vector(self.plane, self.state)
            
        self.pieces += self.plane.step(plane_forces, dt)
            
        #update pieces
        for piece in self.pieces:
            piece_forces = np.array((0.,0.,0.))
            for force in self.forces:
                piece_forces += force.get_force_vector(piece, self.state)
                
            piece.step(piece_forces, dt)
        
        #single state :D
        if self.state == State.initial:
            self.state = State.air
            
        