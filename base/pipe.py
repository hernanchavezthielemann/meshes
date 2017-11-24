#!/usr/bin/python

# simple pipe builder


from numpy import pi, zeros, array, cos, sin
from stl import mesh

def build(radius, height, finishing = 12):
    
    P = 2*pi*radius
    ratio = height/P
    hgt_chunk_qty = int( finishing*ratio)
    return _pipemesh(radius, height, hgt_chunk_qty, finishing)


def _build(radius, height, height_chunks, radial_chunks, theta=0):
    '''lacking verbose again '''
    delta_theta = 360/float(radial_chunks)*(pi/180) # in radians
    
    pipe = zeros( 2*radial_chunks*height_chunks, dtype=mesh.Mesh.dtype)
    
    H = height/float(height_chunks)
    buffer = 0
    R=radius
    for h in range(height_chunks):
        theta = delta_theta*h/2
        for i in range(radial_chunks):
            
            pipe['vectors'][i*2 + buffer] = array([[R*cos(theta), R*sin(theta), H*h],
                                                   [R*cos(theta+delta_theta/2), R*sin(theta+delta_theta/2), H*h+H],
                                                   [R*cos(theta+delta_theta), R*sin(theta+delta_theta), H*h]])
            theta+=delta_theta/2
            
            pipe['vectors'][i*2+1 + buffer] = array([[R*cos(theta), R*sin(theta), H*h+H],
                                                     [R*cos(theta+delta_theta/2), R*sin(theta+delta_theta/2), H*h],
                                                     [R*cos(theta+delta_theta), R*sin(theta+delta_theta), H*h+H]])
            theta += delta_theta/2
        buffer += 2*radial_chunks
        
    return pipe
