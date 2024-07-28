import numpy as np
import math

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
