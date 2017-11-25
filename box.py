#!/usr/bin/python

from stl import mesh
from numpy import concatenate
from base.squared import build_from_diagonal as buildsquare
from utils.render import meshrender



def build(pt1, pt2, finishing):
    
    
    low_x, upr_x = sorted([pt1[0], pt2[0]])
    low_y, upr_y = sorted([pt1[1], pt2[1]])
    low_z, upr_z = sorted([pt1[2], pt2[2]])
    print low_x, upr_x
    print low_y, upr_y
    print low_z, upr_z
    x_dist = upr_x - low_x
    y_dist = upr_y - low_y
    z_dist = upr_z - low_z
    
    vertex= [ low_x, low_y, low_z]
    #=============================================================
    # base   - XY
    data_basemesh = buildsquare(vertex, [upr_x, upr_y, low_z], finishing)
    # ceil   - XY
    data_topmesh = data_basemesh.copy()
    data_topmesh['vectors'] += [ 0, 0, z_dist]
    #=============================================================
    # frontal - XZ
    data_frontsidemesh = buildsquare(vertex, [upr_x, low_y, upr_z], finishing)
    # rear   - XZ
    data_rearsidemesh = data_frontsidemesh.copy()
    data_rearsidemesh['vectors'] += [ 0, y_dist, 0]
    #=============================================================
    # leftside - YZ
    data_leftsidemesh = buildsquare(vertex, [low_x, upr_y, upr_z], finishing)
    # rightside   - YZ
    data_rightsidemesh = data_leftsidemesh.copy()
    data_rightsidemesh['vectors'] += [ x_dist, 0, 0]
    #=============================================================
    meshdata = [ data_basemesh, data_topmesh,
                data_frontsidemesh, data_rearsidemesh,
                data_leftsidemesh, data_rightsidemesh]#
                
    data = concatenate( meshdata)
    return data
    
if __name__ == "__main__":
    
    onemesh = build([ 0, 0, 0], [ 9, 6, 6], 32)
    #onemesh = buildsquare([ 0, 0, 0], [ 6, 6, 0], 64)
    meshes = [mesh.Mesh(onemesh)]
    meshrender( meshes, 0)
