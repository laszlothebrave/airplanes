from random import randint

import numpy as np
from OpenGL.GL import *


class Surface:

    def __init__(self):
        self.vertices = np.zeros((21, 21))
        for x in range(21):
            for y in range(21):
                self.vertices[x][y] = (x-8)*(x-8)*3+(y-11)*(y-11)*2 + randint(0,100)

    def print(self):
        glLineWidth(1)
        glColor3f(0, 1, 0)

        for x in range(20):
            for y in range(20):
                glBegin(GL_LINE_LOOP)
                glVertex3fv((x*100,self.vertices[x][y],y*100))
                glVertex3fv((x*100,self.vertices[x][ y+1],(y+1)*100))
                glVertex3fv(((x+1)*100, self.vertices[x+1][ y],y*100))
                glEnd()
        for x in range(20):
            glBegin(GL_LINE_LOOP)
            glVertex3fv((x * 100, self.vertices[x][20], 2000))
            glVertex3fv(((x + 1) * 100, self.vertices[x + 1][20], 2000))
            glEnd()
        for y in range(20):
            glBegin(GL_LINE_LOOP)
            glVertex3fv((2000, self.vertices[20][y], y * 100))
            glVertex3fv((2000, self.vertices[20][y+1],(y + 1) * 100))
            glEnd()