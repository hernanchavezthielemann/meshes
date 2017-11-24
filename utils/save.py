#!/usr/bin/python

from stl import mesh, stl
from numpy import concatenate

def meshlist2stl(mesh_list):
    
    justonemesh = mesh.Mesh( concatenate( [me.data for me in mesh_list]))
    justonemesh.save('mesh_X_try.stl', mode= stl.Mode.ASCII)
    
//TODO: other save modes??
