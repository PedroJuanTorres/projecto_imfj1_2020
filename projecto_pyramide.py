"""projecto pyramide application"""
import time
import math
import pygame

from quaternion import Quaternion

from scene import Scene
from object3d import Object3d
from camera import Camera
from mesh import Mesh
from material import Material
from color import Color
from vector3 import Vector3

# Define a main function, just to keep things nice and tidy
def main():
    """Main function, it implements the application loop"""
    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res_x = 640
    res_y = 480

    # Create a window and a display surface
    screen = pygame.display.set_mode((res_x, res_y))

    # Create a scene
    scene = Scene("TestScene")
    scene.camera = Camera(False, res_x, res_y)

    # Moves the camera back 2 units
    scene.camera.position -= Vector3(0, 0, 3)

    # Create a sphere and place it in a scene, at position (0,0,0)
    obj1 = Object3d("TestObject")
    obj1.scale = Vector3(1, 1, 1)
    obj1.position = Vector3(0, 0, 0)
    obj1.mesh = Mesh.create_pyramide(7)
    obj1.material = Material(Color(1, 0, 0, 1), "TestMaterial1")
    scene.add_object(obj1)

    # Specify the rotation of the object. It will rotate 15 degrees around the axis given,
    # every second

    # Timer
    delta_time = 0
    prev_time = time.time()

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

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
         
            elif key_state[pygame.K_k]:
                angle = 15
                axis = Vector3(0, 1, 0)
                axis.normalize()
                ax = (axis * math.radians(angle) * 0.2)

                q = Quaternion.AngleAxis(axis, math.radians(angle) * 0.2)
                obj1.rotation = q * obj1.rotation
            elif key_state[pygame.K_LEFT]:
                angle = -15
                axis = Vector3(0, 1, 0)
                axis.normalize()
                ax = (axis * math.radians(angle) * 0.2)

                q = Quaternion.AngleAxis(axis, math.radians(angle) * 0.2)
                obj1.rotation = q * obj1.rotation
            elif key_state[pygame.K_UP]:
                angle = -15
                axis = Vector3(1, 0, 0)
                axis.normalize()
                ax = (axis * math.radians(angle) * 0.2)

                q = Quaternion.AngleAxis(axis, math.radians(angle) * 0.2)
                obj1.rotation = q * obj1.rotation
            elif key_state[pygame.K_DOWN]:
                angle = 15
                axis = Vector3(1, 0, 0)
                axis.normalize()
                ax = (axis * math.radians(angle) * 0.2)

                q = Quaternion.AngleAxis(axis, math.radians(angle) * 0.2)
                obj1.rotation = q * obj1.rotation
            elif key_state[pygame.K_PAGEUP]:
                angle = 15
                axis = Vector3(0, 0, 2)
                axis.normalize()
                ax = (axis * math.radians(angle) * 0.2)

                q = Quaternion.AngleAxis(axis, math.radians(angle) * 0.2)
                obj1.rotation = q * obj1.rotation
            elif key_state[pygame.K_PAGEDOWN]:
                angle = -15
                axis = Vector3(0, 0, 1)
                axis.normalize()
                ax = (axis * math.radians(angle) * 0.2)

                q = Quaternion.AngleAxis(axis, math.radians(angle) * 0.2)
                obj1.rotation = q * obj1.rotation
            elif key_state[pygame.K_w]:
                obj1.position=Vector3(obj1.position.x,obj1.position.y+0.01,obj1.position.z)
            elif key_state[pygame.K_s]:
                obj1.position=Vector3(obj1.position.x,obj1.position.y-0.01,obj1.position.z)
            elif key_state[pygame.K_a]:
                obj1.position=Vector3(obj1.position.x-0.01,obj1.position.y,obj1.position.z)
            elif key_state[pygame.K_d]:
                obj1.position=Vector3(obj1.position.x+0.01,obj1.position.y,obj1.position.z)
            elif key_state[pygame.K_q]:
                obj1.position=Vector3(obj1.position.x,obj1.position.y,obj1.position.z+0.01)
            elif key_state[pygame.K_e]:
                obj1.position=Vector3(obj1.position.x,obj1.position.y,obj1.position.z-0.01)

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0, 0, 0))

        # Rotates the object, considering the time passed (not linked to frame rate)
        

        scene.render(screen)
        # Swaps the back and front buffer, effectively displaying what we rendered
        pygame.display.flip()

        # Updates the timer, so we we know how long has it been since the last frame
        delta_time = time.time() - prev_time
        prev_time = time.time()


# Run the main function
main()
