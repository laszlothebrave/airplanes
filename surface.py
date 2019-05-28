from random import randint

import numpy as np
from OpenGL.GL import *

def clamp(min_v, x, max_v):
    return min(max_v, max(x, min_v))

size = 31

scale = 1000

class Surface:

    def __init__(self):
        self.vertices = np.zeros((size, size))
        for x in range(size):
            for y in range(size):
                self.vertices[x][y] = (x-8)*(x-8)*2+(y-11)*(y-11)*2 + randint(0, 500)

    def print(self):
        glLineWidth(1)
        glColor3f(0, 1, 0)

        for x in range(size-1):
            for y in range(size-1):
                glBegin(GL_LINE_LOOP)
                glVertex3fv((x*scale,self.vertices[x][y],y*scale))
                glVertex3fv((x*scale,self.vertices[x][ y+1],(y+1)*scale))
                glVertex3fv(((x+1)*scale, self.vertices[x+1][ y],y*scale))
                glEnd()
        for x in range(size-1):
            glBegin(GL_LINE_LOOP)
            glVertex3fv((x * scale, self.vertices[x][size - 1], (size-1)*scale))
            glVertex3fv(((x + 1) * scale, self.vertices[x + 1][size - 1], (size-1)*scale))
            glEnd()
        for y in range(size-1):
            glBegin(GL_LINE_LOOP)
            glVertex3fv(((size-1)*scale, self.vertices[20][y], y * scale))
            glVertex3fv(((size-1)*scale, self.vertices[20][y+1],(y + 1) * scale))
            glEnd()
            
    def is_below(self, coords):
        c_round = np.round(coords/scale).astype(np.int)
        
        x_i = clamp(0,c_round[0], size-1)
        y_i = clamp(0,c_round[1], size-1)
        
        return coords[2] < self.vertices[x_i, y_i]