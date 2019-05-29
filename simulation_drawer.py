import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tkinter import *
import threading
import numpy
import numpy as np

from piece import Piece
from surface import Surface

import numpy as np
from airplane import Airplane
from simulation import Simulation

vertices=(
    (10000,-1,10000),
    (10000,-1,-10000),
    (-10000,-1,-10000),
    (-10000,-1,10000)
    )

edges = (
    (0,1),
    (1,2),
    (2,3),
    (3,0)
)


def Pyramid():
    glLineWidth(5)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
            glColor3f(0,1,0)
    glEnd()



def IdentityMat44():
    return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')



def create_surface(size, mountains_number, average_mountain_height, valleys_number, average_valley_deep):
    pass

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        quitButton = Button(self, text="Quit", command=self.client_exit)
        quitButton.place(x=0, y=0)

    def client_exit(self):
        exit()

class myThread (threading.Thread):

   def __init__(self):
      threading.Thread.__init__(self)

   def run(self):
       self.root = Tk()
       self.root.geometry("400x300")
       self.app = Window(self.root)
       self.root.mainloop()
       
   def close(self):
       self.root.quit()
       self.app.quit()

surface = Surface()

plane = Airplane(100000, 100, 15)
airplane = plane
plane.position = np.array((0., 0., 10000.))
plane.velocity = np.array((150., 150., 2.))
sim = Simulation(plane, surface)


pygame.init()
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

tx = 0
ty = 0
tz = 0
ry = 0
rz = 0

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 100000.0)

view_mat = IdentityMat44()
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0, -2000, -14000)
glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
glLoadIdentity()
glRotatef(100, 1, 1, 1)

clock = pygame.time.Clock()
gui = myThread()
gui.start()
threads = []
threads.append(gui)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gui.close()
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gui.close()
                pygame.quit()
                quit()
            if event.key == pygame.K_a:
                tx = 0.1
            elif event.key == pygame.K_d:
                tx = -0.1
            elif event.key == pygame.K_w:
                tz = 0.1
            elif event.key == pygame.K_s:
                tz = -0.1
            elif event.key == pygame.K_RIGHT:
                ry = 1.0
            elif event.key == pygame.K_LEFT:
                ry = -1.0
            elif event.key == pygame.K_DOWN:
                rz = 1.0
            elif event.key == pygame.K_UP:
                rz = -1.0
            elif event.key == pygame.K_EQUALS:
                i = 0
                while not sim.all_landed() and i < 250:
                    sim.step(0.2)
                    i += 1
                    print(plane.position)
            elif event.key == pygame.K_MINUS:
                sim.step(0.2)
                print(plane.position)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a and tx > 0:
                tx = 0
            elif event.key == pygame.K_d and tx < 0:
                tx = 0
            elif event.key == pygame.K_w and tz > 0:
                tz = 0
            elif event.key == pygame.K_s and tz < 0:
                tz = 0
            elif event.key == pygame.K_RIGHT and ry > 0:
                ry = 0.0
            elif event.key == pygame.K_LEFT and ry < 0:
                ry = 0.0
            elif event.key == pygame.K_UP and rz < 0:
                rz = 0.0
            elif event.key == pygame.K_DOWN and rz > 0:
                rz = 0.0
            elif event.key == pygame.K_MINUS:
                sim.step(0.2)
                print(plane.position)
    
    #glPushMatrix()
    glLoadIdentity()
    glTranslatef(tx*1000, ty*1000, tz*1000)
    glRotatef(ry*1, 0, 1, 0)
    glRotatef(rz*1, 1, 0, 0)
    
    glMultMatrixf(view_mat)
    
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #Pyramid()
    
    for piece in sim.pieces:
        piece.draw()
    
    airplane.draw()
    surface.print()
    #glPopMatrix()
    
    pygame.display.flip() 
