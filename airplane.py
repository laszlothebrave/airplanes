from piece import Piece
import random
import numpy as np

from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f
from OpenGL.raw.GLU import gluSphere
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from PIL import Image as Image
import numpy

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
    
    def draw(self):
        glPushMatrix()
        if self.state == 0:
            glColor3f(1, 0, 1)
        else:
            glColor3f(1, 1, 1)
        qobj = gluNewQuadric()
        
        glTranslatef(self.position[0], self.position[2], self.position[1])
        gluSphere(qobj, 40, 10, 10)
        glPopMatrix()
    
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