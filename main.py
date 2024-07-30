import pygame
import object_3d as obj
import camera as cam
import projection as proj
import math


class Render:
    def __init__(self):
        # starts application window
        pygame.init()
        self.RES = self.WIDTH, self.HEIGHT = 1920, 1080
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.fps = 144
        # creates fps counter
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.create_objects()

    def create_objects(self):
        # creates and sets initial position of camera, objects etc.
        self.camera = cam.Camera(self, [40, 160, -900])
        self.projection = proj.Projection(self)
        self.object = self.get_object_from_file("objects/cat.obj")
        self.object.rotate_y(math.pi / 4)
        self.object.rotate_x(-math.pi / 10)

    # stores and transforms .obj files for use by the engine
    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            # list comprehensions for simplifying data transformation
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return obj.Object3D(self, vertex, faces)

    def draw(self):
        # paints background
        self.screen.fill("cadetblue4")
        self.object.draw()

    def run(self):
        # program loop
        while True:
            self.draw()
            self.camera.control()
            # event handler
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    engine = Render()
    engine.run()
