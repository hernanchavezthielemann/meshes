#!/usr/bin/python

from stl import mesh
from numpy import pi

def mesh_randcrea( base_mesh):
    ''' working on it.... at the moment is yust nothing more
    than a work bench'''
    meshes = [mesh.Mesh( base_mesh.copy()) for _ in range(11)]
    
    # Rotate 90 degrees over the Y axis
    meshes[0].rotate([0.0, 0.5, 0.0], 90*pi/180)
    meshes[0].x -= 20
    meshes[0].y += 140
    # Translate 10 points over the X axis
    meshes[1].x += 150
    meshes[1].y -= 150
    meshes[1].rotate([0.0, 0.5, 0.0], -30*pi/180)
    # Rotate 45 degrees over the X axis
    # Translate 10 points over the X axis
    meshes[2].rotate([0.5, 0.0, 0.0], 45*pi/180)
    meshes[2].x += 10
    meshes[2].y += 130
    
    # Rotate 120 degrees over the X and Y axis
    meshes[3].rotate([0.5, 0.0, 0.0], 120*pi/180)
    meshes[3].rotate([0.0, 0.5, 0.0], 120*pi/180)
    # Translate 10 points over the Y and X axis
    meshes[3].x += 100
    meshes[3].y += 100
    
    
    meshes[4].rotate([0.0, 0.5, 0.0], 260*pi/180)
    meshes[4].x -= 150
    # Translate 10 points over the X axis
    meshes[5].x += -100
    meshes[5].y -= 200
    meshes[5].rotate([0.0, 0.5, 0.0], -70*pi/180)

    # Rotate 45 degrees over the X axis
    # Translate 10 points over the X axis
    meshes[6].rotate([0.5, 0.0, 0.0], 45*pi/180)
    meshes[6].x += 160
    meshes[6].y += 130
    meshes[9].z += 100
    
    # Rotate 120 degrees over the X and Y axis
    meshes[8].x -= 160
    meshes[7].rotate([0.5, 0.0, 0.0], 120*pi/180)
    meshes[7].rotate([0.0, 0.5, 0.0], 120*pi/180)
    # Translate 10 points over the Y and X axis
    meshes[8].x += 160
    meshes[8].y -= 100
    meshes[8].z -= 100
    # Rotate 45 degrees over the X axis
    # Translate 10 points over the X axis
    meshes[9].rotate([0.5, 0.0, 0.0], 45*pi/180)
    meshes[9].x -= 110
    meshes[9].y -= 130
    meshes[9].z += 100
    
    return meshes
    
