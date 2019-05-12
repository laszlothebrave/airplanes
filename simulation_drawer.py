import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from tkinter import *
import threading


vertices=(
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (0,0,1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (1,4),
    (1,2),
    (2,4),
    (2,3), # (2,3)
    (3,4)
)


def Pyramid():
    glLineWidth(5)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
            glColor3f(0,1,0)
    glEnd()

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
       root = Tk()
       root.geometry("400x300")
       app = Window(root)
       root.mainloop()


def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50)

    glTranslatef(0,0,-10)

    clock = pygame.time.Clock()
    gui = myThread()
    gui.start()
    threads = []
    threads.append(gui)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 1, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Pyramid()
        pygame.display.flip()


main()