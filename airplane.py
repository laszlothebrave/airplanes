from piece import Piece
import random

class Airplane(Piece):
    def __init__(self, mass, pieces):
        super().__init__()
        self.mass = mass
        self.pieces_left = pieces
        
    def step(self, forces_sum, dt):
        #generate pieces
        super().step(forces_sum, dt)
        return self._new_pieces()
    
    def _new_pieces(self):
        new_pieces_num = int(random.uniform(0, self.pieces_left))
        new_pieces = []
        for i in range(new_pieces_num):
            piece = Piece()
            piece.explode(self, self.mass/2, 50, 50)
            self.mass -= piece.mass
            new_pieces.append(piece)
        
        return new_pieces