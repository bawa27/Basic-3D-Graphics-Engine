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
        # sets initial position of camera, objects etc.
        self.camera = cam.Camera(self, [0.5, 1, -4])
        self.projection = proj.Projection(self)
        self.object = obj.Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])
        self.object.rotate_y(math.pi/6)

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


def main():
    engine = Render()
    engine.run()


if __name__ == '__main__':
    main()
