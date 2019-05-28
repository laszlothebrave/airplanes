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

def clamp(min_v, x, max_v):
    return min(max_v, max(x, min_v))

class Piece:
    def __init__(self):
        self.position = np.array((0, 0, 0), dtype = np.float64)
        self.mass = 0
        self.velocity = np.array((0, 0, 0), dtype = np.float64)
        self.air_friction_factor = 0
        self.springiness = 0
        self.ground_friction_factor = 0
        
    def explode(self, plane, max_mass, rnd_mu, rnd_sigma):
        self.position = plane.position
        self.velocity = plane.velocity + random.gauss(rnd_mu, rnd_sigma)
        self.mass = random.uniform(1, max_mass)
        self.air_friction_factor = random.random()
        
    def step(self, forces_sum, dt):
        self._update_velocity(forces_sum, dt)
        self._update_position(dt)

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


        glColor3f(1, 0, 0)
        qobj = gluNewQuadric()
        
        glTranslatef(self.position[0], self.position[2], self.position[1])
        gluSphere(qobj, 50, 50, 50)

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
    
    def _update_velocity(self, forces_sum, dt):
        self.velocity += forces_sum * dt

    def _update_position(self, dt):
        self.position += self.velocity * dt