import numpy as np
import math
import pygame
import matrix_functions as matrix

# defining the camera and switching to "camera space" or the camera view coordinate system

class Camera:
    def __init__(self, render, position):
        self.render = render
        # "*" unpacks the position variable
        self.position = np.array([*position, 1.0])
        self.z_move = np.array([0, 0, 1, 1])
        self.y_move = np.array([0, 1, 0, 1])
        self.x_move = np.array([1, 0, 0, 1])
        self.h_fov = math.pi/3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.move_speed = 0.02
        self.rotate_speed = 0.005

    # using pygame movement commands to move the camera on keypress
    def control(self):
        key = pygame.key.get_pressed()

        # translation
        if key[pygame.K_a]:
            self.position -= self.x_move * self.move_speed
        if key[pygame.K_d]:
            self.position += self.x_move * self.move_speed
        if key[pygame.K_w]:
            self.position += self.z_move * self.move_speed
        if key[pygame.K_s]:
            self.position -= self.z_move * self.move_speed
        if key[pygame.K_q]:
            self.position += self.y_move * self.move_speed
        if key[pygame.K_e]:
            self.position -= self.y_move * self.move_speed

        # rotation
        if key[pygame.K_LEFT]:
            self.camera_yaw(-self.rotate_speed)
        if key[pygame.K_RIGHT]:
            self.camera_yaw(self.rotate_speed)
        if key[pygame.K_UP]:
            self.camera_pitch(-self.rotate_speed)
        if key[pygame.K_DOWN]:
            self.camera_pitch(self.rotate_speed)
        if key[pygame.K_r]:
            self.camera_roll(self.rotate_speed)
        if key[pygame.K_f]:
            self.camera_roll(-self.rotate_speed)

    # rotating the camera
    def camera_yaw(self, angle):
        rotate = matrix.rotate_y(angle)
        self.z_move = self.z_move @ rotate
        self.x_move = self.x_move @ rotate
        self.y_move = self.y_move @ rotate

    def camera_pitch(self, angle):
        rotate = matrix.rotate_x(angle)
        self.z_move = self.z_move @ rotate
        self.x_move = self.x_move @ rotate
        self.y_move = self.y_move @ rotate

    def camera_roll(self, angle):
        rotate = matrix.rotate_z(angle)
        self.z_move = self.z_move @ rotate
        self.x_move = self.x_move @ rotate
        self.y_move = self.y_move @ rotate

    # used to move the world so that the camera position coincides with the origin of the world coordinate system
    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1],
        ])

    # Note that the matrix functions below are camera-specific
    # They are different from the ones present in matrix_functions.py

    # used to rotate the camera system to orient it relative to the world coordinate system (the object's system)
    def rotate_matrix(self):
        rx, ry, rz, w = self.x_move
        fx, fy, fz, w = self.z_move
        yx, yy, yz, w = self.y_move

        return np.array([
            [rx, yx, fx, 0],
            [ry, yy, fy, 0],
            [rz, yz, fz, 0],
            [0, 0, 0, 1]
        ])

    # final matrix multiplication operation to switch to camera space
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
