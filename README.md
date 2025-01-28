# A Basic 3D Graphics Engine in Python

![program_image](https://github.com/user-attachments/assets/9c02e6d0-7fc1-4422-ac5c-8a5440a5dc6e)

## Overview:
The idea for this stemmed from a much larger one - the creation of a whole physics engine capable of visualizing complex concepts like general relativity and quantum mechanics. Of course, this is far from that, but this project was mostly intended to be a hands-on way to learn how 3D graphics work. From here, I'm going to build up to this much more complex idea. Ultimately, it was a fun little mini-project that was a culmination of what I learned about 3D graphics in a few days of studying. Below is a list of all of the important files and what they do:

- **main.py** = starts the engine and uses every other class
- **camera.py** = handles camera movement
- **matrix_functions.py** = matrix transforms used to move the object in space
- **object_3d** = allows .obj files to be loaded into the engine
- **projection.py** = a set of matrix transforms that move the scene from "camera space" to "clip space" (explained further on)

## Quickstart:
Clone onto your system and run main.py. 

WASD controls for moving forward, left, backward, and right.  
Q, E to move up and down.  
Arrow keys + K and F for rotation and rolling.  

To load your own .obj files, put the .obj file in the objects folder in the resources directory and change line 24 of main.py like so:  
"resources/objects/<your_file>.obj"

## How It's Made:
Before I started writing code, I did a lot of research about how 3D graphics works, and how it can be implemented in python. I quickly discovered that a full engine was difficult to build alone due to python's automatic garbage collection. Still, my familiarity with python and its simplicity lent well to the process of learning about 3D graphics.

3D graphics works by essentially tricking your brain into thinking that a 2D object is 3D, similar to how a good artist can create incredibly realistic drawings. I always found the easiest 3D object to draw was a cube, so I started with that. I inputted the coordinates of a cube's edges and defined its faces with the indices of those coordinates, similar to how .obj files define objects but not with the same format. With my object defined, I had to run it through the camera space and perspective projection transformation matrices. I defined the perspective transform matrices together in the projection.py files. The basic logic required and matrices themselves came from some Youtube and textbooks about the math behind 3D graphics.

I defined my camera matrix along with the camera class itself, as well as the required rotation and translation matrices. I multiplied these matrices by the coordinates of all the vertices to switch to clip space. To clip I divided all vertices by the clip space's width and set all values greater than 1 or less than -1 to 0, effectively removing/not rendering them. I then projected flat to a 2D screen by removing the z column entirely, which is workable for this simple engine.

I then looped through the vertices and lines between ones that were not clipped, thus drawing only faces that had all of their vertices in the clip space. I also made some translation and rotation matrices for the object, put these into matrix_functions.py, and created functions for them in the object.py file. Finally, I combined all of these classes into main.py, which creates the objects, background, camera, and application window and handles events. This first version didn't have any events, as I just wanted to see if I handled my matrix operations correctly. After some tweaks, I had a working cube. 

I added rotation and movement soon after using some simple pygame keypress handlers, and I added .obj file support soon after. However, since these obj files had many vertices that all needed to be calculated at once, I was experiencing severe frame loss. Through some searching, I found someone with a similar issue who had found that the numpy.any method is a bottleneck for large datasets needing to be passed quickly. To fix it, they used the numba JIT compiler to speed up the math on this operation. This was a quick and dirty solution, but I was just about done with the program at this point and felt that I had gotten a good idea of the code behind a 3D engine. 

## Lessons Learned:
I learned a lot about 3D graphics through this project, and that was my goal. I haven't had much exposure to this side of programming before, but it was very interesting to dive into it. This engine uses object order rendering, which draws objects in 3D space but uses a series of matrix transforms to flatten them out and draw them on top of eachother in a way that tricks our brains into thinking they are 3D. This is opposed to image order rendering or ray tracing, which "shoots" rays out of the camera, bounces them off of objects, and computes lighting in real-time.

Object order rendering starts in world space, where everything is defined by a 3D world coordinate system. Of course, only a certain region of objects can be rendered onto the screen at a time, and this is known as the canonical viewing volume (CVV). Objects within this volume are in clip space. Everything outside is "clipped" - not rendered until it is inside the viewing volume. The ultimate goal of clip space is to take everything within the box and project it onto the plane opposite of the screen in the CVV, making it flat. To do so, there are three important matrices that are required: the camera space matrix, the perspective transformation matrix, and the orthographic transformation matrix. 

The camera space matrix goes from a universal coordinate system to a coordinate system relative to the camera. This is required for my engine as the world moves around the camera instead of the other way around. The perspective transformation matrix adds depth to an image, and it is modeled with a viewing frustum rather than a rectangle. Orthographic transformations map this frustum to the CVV, making further objects smaller relative to closer ones while also being the correct shape. These last two matrices multiplied together yield the perspective projection transformation matrix, and all of them multiplied yield the CVV. A final viewport matrix is also required to transform the CVV units to screen units.

Besides these matrices, there are also matrices for object translation, rotation, and scaling. When used together they can simulate movement around a 3D object realistically. 
