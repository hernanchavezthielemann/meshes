#!/usr/bin/python

from sys import argv
from stl import mesh, stl
from numpy import pi, sin, cos, zeros, array, concatenate

import base.pipe as pipemesh
import base.circle as circlemesh
from utils.render import meshrender
from utils.save import meshlist2stl

def build_cylindricalmesh(radius, height, finishing):
    ''' builds a cylindrical mesh starting on (0, 0, 0)... lacking verbose
    '''
    #=============================================================
    #       Lower cap
    data_lower_cap, angular_chunk_qty, core_qty = circlemesh.build(radius,
                                                                   finishing,
                                                                   True)
    P = 2*pi*radius
    ratio = height/P
    hgt_chunk_qty = int( angular_chunk_qty*ratio)
    if hgt_chunk_qty%2<>0:
        hgt_chunk_qty-=1
    #=============================================================
    #       Pipe
    data_pipe = pipemesh._build(radius, height, hgt_chunk_qty, angular_chunk_qty)
    #       Upper cap
    data_upper_cap = data_lower_cap.copy()
    data_upper_cap['vectors'] += [ 0, 0, height]
    #=============================================================
    mshdata_con = [data_lower_cap, data_pipe, data_upper_cap]
    comb1 = concatenate( mshdata_con)#[ msh_data for msh_data in mshdata_con])
    return comb1

#------------------------------------------------------
#///////////////     Main             /////////////
#------------------------------------------------------

if __name__ == "__main__":
    
    
    #====================================================================
    #==============         TEST PARAMETERS     =========================
    finish = 20
    radius = 7
    height = 85
    
    selector = 2 # 0 - 1 - 2
    
    if len(argv)>1 and argv[1]=='-h':
        print('''
Syntax python cylinder.py <args>
                           args: finish radius height selector
                                
                                finish  :  mesh grid finishing
                                selector:  0 : just a pipe
                                           1 : just a cap
                                           2 : a whole cylinder (defval)
       Eg.: python cylinder.py 12 7 100
                ''')
    
    elif len(argv)>1:
        finish = int(argv[1])
        if len(argv)>2:
            radius = int(argv[2])
        if len(argv)>3:
            height = int(argv[3])
        if len(argv)>4:
            selector = int(argv[4])
            
        #====================================================================
        if selector == 2:
            cylinder = build_cylindricalmesh( radius, height, finish)
            #meshes = mesh_randcrea( cylinder)
            meshes = [mesh.Mesh(cylinder)]
            meshlist2stl( meshes)
            meshrender( meshes)
        else:
            P = 2*pi*radius
            angular_chunk_qty, core_qty = circlemesh.finishing2size( finish)
            
            ratio = height/P
            hgt_chunk_qty = int( angular_chunk_qty*ratio)
            
            if selector:
                onemesh = circlemesh._build(radius, angular_chunk_qty, core_qty)
            else:
                onemesh = pipemesh._build(radius, height, hgt_chunk_qty, angular_chunk_qty)
                
            meshes = [mesh.Mesh(onemesh)]
            meshrender( meshes,0)
