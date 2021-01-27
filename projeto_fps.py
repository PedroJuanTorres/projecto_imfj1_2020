"""Game sample application"""

import time
import random
import math
import pygame

from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3, dot_product, cross_product
from quaternion import Quaternion
from perlin import noise2d


# Computes the height of the terrain at the given x,y point
def sample_height(x, y):
    """Samples a pseudo heighmap, built with 2-octaves of 2d perlin noise. This is
    clamped near the player, so we have a nice flat area near him. We also clamp it to
    values above 0, so it looks more natural"""
    # 2 octave noise, with a given scale
    scale_noise = 0.4
    noise_height = 5
    n = 0.5 * noise2d(x * scale_noise, y * scale_noise)
    n += 0.25 * noise2d(x * scale_noise * 2, y * scale_noise * 2)
    n *= noise_height
    if ((n < 0) or (y < 8)):
        n = 0

    return n

def create_terrain():
    """Creates a terrain to use as a background in the game"""
    # Size of the terrain
    size_x = 16
    size_z = 16
    # Number of divisions of the terrain. Vertex count scales with the square of this
    div = 20

    px = size_x / div
    pz = size_z / div

    # For centering the terrain on the object center
    origin = Vector3(-size_x * 0.5, 0, 0)

    terrain_mesh = Mesh("Terrain")

    # Create the geometry of the terrain and add it to the mesh
    for dz in range(0, div):
        for dx in range(0, div):
            p1 = Vector3(dx * px, 0, dz * pz) + origin
            p2 = Vector3((dx + 1) * px, 0, dz * pz) + origin
            p3 = Vector3((dx + 1) * px, 0, (dz + 1) * pz) + origin
            p4 = Vector3(dx * px, 0, (dz + 1) * pz) + origin

            p1.y = sample_height(p1.x, p1.z)
            p2.y = sample_height(p2.x, p2.z)
            p3.y = sample_height(p3.x, p3.z)
            p4.y = sample_height(p4.x, p4.z)

            poly = []
            poly.append(p1)
            poly.append(p2)
            poly.append(p3)
            poly.append(p4)

            terrain_mesh.polygons.append(poly)

    # Create materials for the terrain
    terrain_material = Material(Color(0.1, 0.6, 0.1, 1), "TerrainMaterial")

    # Create object to display the terrain
    obj = Object3d("TerrainObject")
    obj.scale = Vector3(1, 1, 1)
    obj.position = Vector3(0, -1, 1)
    obj.mesh = terrain_mesh
    obj.material = terrain_material

    return obj

def main():
    """Main function, it implements the application loop"""

    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 1280
    res_y = 720

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")
    scene.camera = Camera(False, res_x, res_y)

    # Moves the camera back 2 units
    scene.camera.position -= Vector3(0, 0, 0)

    # Creates the terrain meshes and materials
    terrain_object = create_terrain()
    scene.add_object(terrain_object)

    # Timer
    delta_time = 0
    prev_time = time.time()


    # Game loop, runs forever
    while True:
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if event.type == pygame.QUIT:
                # Exits the application immediately
                return
            key_state = pygame.key.get_pressed()
            if key_state[pygame.K_ESCAPE]:
                return
            if key_state[pygame.K_d]:
                scene.camera.position = Vector3(scene.camera.position.x+0.1,scene.camera.position.y,scene.camera.position.z)
            if key_state[pygame.K_a]:
                scene.camera.position = Vector3(scene.camera.position.x-0.1,scene.camera.position.y,scene.camera.position.z)
            if key_state[pygame.K_w]:
                scene.camera.position = Vector3(scene.camera.position.x,scene.camera.position.y,scene.camera.position.z+0.1)
            if key_state[pygame.K_s]:
                scene.camera.position = Vector3(scene.camera.position.x,scene.camera.position.y,scene.camera.position.z-0.1)
        
        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 20))

      

        # Render scene
        scene.render(screen)

       

        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()

# Run the main function
main()

