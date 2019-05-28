from piece import Piece
import random
import numpy as np

class Airplane(Piece):
    def __init__(self, mass, pieces, tmax):
        super().__init__()
        self.t = 0
        self.tmax = tmax
        self.times = np.random.uniform(0, tmax, size = (pieces))
        
        self.max_mass = mass/ 2 / pieces
        
        self.mass = mass
        self.pieces_left = pieces
        
    def step(self, forces_sum, dt):
        #generate pieces
        self.t += dt
        super().step(forces_sum, dt)
        return self._new_pieces()
    
    def _new_pieces(self):
        new_pieces = []
        
        to_spawn = self.times < self.t
        self.times = np.delete(self.times, to_spawn)
        num = np.sum(to_spawn)
        
        for i in range(num):
            piece = Piece()
            piece.explode(self, self.max_mass, 25, 25)
            self.mass -= piece.mass
            self.pieces_left -= 1
            new_pieces.append(piece)
            
        return new_pieces