import pyglet
from pyglet.gl import *
from pyglet.window import key
from pyglet.clock import schedule_interval
from pycube import Cube
from pycube import solver


class CubeWindow(pyglet.window.Window):
    def __init__(self, cube_size=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glEnable(GL_DEPTH_TEST)
        self.set_minimum_size(300, 300)
        self.cube = Cube(cube_size)
        self.cube.scramble()
        self.cube_batch = self.cube.create_batch()
        self.cube_solver = solver.CFOPSolver(self.cube)

        # Camera parameters
        self.camera_pos = (4, 4, 4)
        self.target_pos = (0, 0, 0)
        self.up_vector = (0, 1, 0)

        # Schedule the update of the window at 60 FPS
        schedule_interval(self.update, 1/60)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*self.camera_pos, *self.target_pos, *self.up_vector)
        self.cube_batch.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        return True

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.cube.rotate("L")
        elif symbol == key.RIGHT:
            self.cube.rotate("R")
        elif symbol == key.UP:
            self.cube.rotate("U")
        elif symbol == key.DOWN:
            self.cube.rotate("D")
        elif symbol == key.Q:
            self.cube.rotate("F")
        elif symbol == key.A:
            self.cube.rotate("B")
        elif symbol == key.SPACE:
            self.cube.scramble()
        elif symbol == key.ENTER:
            self.cube_solver.solve()
        elif symbol == key.ESCAPE:
            pyglet.app.exit()

    def update(self, dt):
        self.cube_batch.delete()
        self.cube_batch = self.cube.create_batch()
        if self.cube.is_solved():
            print("Cube solved!")


if __name__ == "__main__":
    window = CubeWindow(3, 800, 600, "Rubik's Cube Solver")
    pyglet.app.run()
