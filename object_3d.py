import numpy as np
import pygame
import matrix_functions as matrix


# this class creates a cube in three dimensions using the inputted vertices


class Object3D:
    def __init__(self, render):
        self.render = render
        # these coordinates are in the world/object coordinate system
        self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])

        # each entry here is a different face of the cube based on the coordinates above
        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1),
                               (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        # switching to camera space
        vertices = self.vertices @ self.render.camera.camera_matrix()
        # switching to clip space
        vertices = vertices @ self.render.projection.projection_matrix
        # switching to normalized device (NDC) space by dividing by the clip space w value
        vertices /= vertices[:, -1].reshape(-1, 1)
        # clipping off vertices >1 or <-1
        vertices[(vertices > 1) | (vertices < -1)] = 0
        # projecting to 2D screen space
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        # getting only the vertices to draw faces that haven't been cut off
        for face in self.faces:
            polygon = vertices[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pygame.draw.polygon(self.render.screen, pygame.Color("red"), polygon, 3)

        for vertex in vertices:
            if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                pygame.draw.circle(self.render.screen, pygame.Color("white"), vertex, 6)

    # here, methods for transforming the object in space are outlined using the appropriate matrix
    # "@" is the same as the numpy matrix multiplication operation
    def translate(self, pos):
        self.vertices = self.vertices @ matrix.translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ matrix.scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ matrix.rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ matrix.rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ matrix.rotate_z(angle)
