import numpy as np
import random
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f
from OpenGL.raw.GLU import gluSphere
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from PIL import Image as Image
import numpy
import numba

def clamp(min_v, x, max_v):
    return min(max_v, max(x, min_v))

class Piece:
    def __init__(self):
        self.state = 0
        self.position = np.array((0, 0, 0), dtype = np.float64)
        self.mass = 0
        self.velocity = np.array((0, 0, 0), dtype = np.float64)
        self.air_friction_factor = 0.8
        self.springiness = 0
        self.ground_friction_factor = 0
        
        
    def explode(self, plane, max_mass, rnd_mu, rnd_sigma):
        self.position = plane.position.copy()
        self.velocity = plane.velocity.copy() + np.random.normal(rnd_mu, rnd_sigma,(3))
        self.mass = random.uniform(1, max_mass)
        self.air_friction_factor = random.uniform(0.2, 1)
    
    def step(self, forces_sum, dt):
        #print("forces: ", forces_sum)
        if self.state == 0:
            self._update_velocity(forces_sum, dt)
            self._update_position(dt)
            
    @numba.jit()
    def draw(self):
        # tex = self.read_texture('sphere_image.jpg')
        # qobj = gluNewQuadric()
        # gluQuadricTexture(qobj, GL_TRUE)
        # glEnable(GL_TEXTURE_2D)
        # glBindTexture(GL_TEXTURE_2D, tex)
        # glBegin(GL_TRIANGLES)
        # gluSphere(qobj, 1, 50, 50)
        # gluDeleteQuadric(qobj)
        # glDisable(GL_TEXTURE_2D)
        #
        # color = [1.0, 0.0, 0.0, 1.0]
        # glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        # glTranslatef(-2, 0, 0)
        # glutSolidSphere(1, 100, 20)
        glPushMatrix()
        if self.state == 0:
            glColor3f(1, clamp(0.,self.mass / 1000,1.), 0)
        else:
            glColor3f(1, 1, 1)
        qobj = gluNewQuadric()
        
        glTranslatef(self.position[0], self.position[2], self.position[1])
        gluSphere(qobj, 20, 10, 10)
        glPopMatrix()

    def read_texture(self, filename):
        img = Image.open(filename)
        img_data = numpy.array(list(img.getdata()), numpy.int8)
        textID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textID)  # This is what's missing

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        return textID
    
    @numba.jit()
    def _update_velocity(self, forces_sum, dt):
        self.velocity += forces_sum * dt / self.mass
   
    @numba.jit()
    def _update_position(self, dt):
        self.position += self.velocity * dt