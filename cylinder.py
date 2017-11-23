#!/usr/bin/python

from sys import exit, argv
from stl import mesh, Dimension, stl
from numpy import pi, ceil, sin, cos, zeros, array, concatenate

def fac(num):
    fa=1
    for x in range(num):
        fa*=(1+x)
    return fa

def finishing2size(num):
    
    core_list = range(10)[3:]
    c_list = []
    flag = False
    core = 0
    if num < 6:
        num = 6
        core = 3
        flag = True
    if not flag:
        for n in core_list:
            c_list.append(n*2)
            if num <= n*2:
                num=n*2
                core = n
                flag = True
                break
    if not flag:
        for n in c_list:
            c_list.append(n*2)
            if num <= n*2:
                num = n*2
                flag = True
                core = n
                while core not in core_list:
                    core /= 2
                break
            elif n*2>1000:
                exit('Warning!! ceil reached')
    return num, core

def build_cylindricalmesh(radius, height, finishing):
    ''' builds a cylindrical mesh starting on (0, 0, 0)... lacking verbose
    '''
    
    P = 2*pi*radius
    angular_chunk_qty, core_qty = finishing2size( finishing)
    ratio = height/P
    hgt_chunk_qty = int( angular_chunk_qty*ratio)
    if hgt_chunk_qty%2<>0:
        hgt_chunk_qty-=1
    #=============================================================
    #       Pipe
    data_pipe = build_pipemesh(radius, height, hgt_chunk_qty, angular_chunk_qty)
    #=============================================================
    #       Lower cap
    data_lower_cap = buid_circlemesh(radius, angular_chunk_qty, core_qty)
    #       Upper cap
    data_upper_cap = data_lower_cap.copy()
    data_upper_cap['vectors'] += [ 0, 0, height]
    #=============================================================
    mshdata_con = [data_lower_cap, data_pipe, data_upper_cap]
    comb1 = concatenate( mshdata_con)#[ msh_data for msh_data in mshdata_con])
    return comb1

def buid_circlemesh(radius, angular_chunks, core_num, ch = 0):
    ''' quite neat and nice method to build circular meshes'''
    #===================================================
    P = 2*pi*radius
    radial_chnk_len = P/(2*angular_chunks)#             eg. 1.099 = 43/(2*20)
    radial_steps = int((radius/radial_chnk_len) - 1)
    if (radius/radial_chnk_len-1)<2:
        radial_steps = 2
    radial_chnk_len = radius/float(radial_steps)
    
    coef_2x_repeatnum = angular_chunks/core_num#        eg.  4   = 20/5
    repeatnum = 1
    while coef_2x_repeatnum/2 <>1:
        coef_2x_repeatnum /= 2
        repeatnum += 1  # 1 2 3 4 ....      eg.  2   = 4/2 --> 1   = 2/2 end with repeatnum == 2
        
    layers2comp = 0
    flag_2cover = False
    if radial_steps > repeatnum + 1:
        layers2comp = radial_steps- repeatnum- 1
        if layers2comp<>0 and layers2comp%2<>0:
            flag_2cover = True
            r2cover = radial_chnk_len*layers2comp
            layers2comp+=1
    tap_tri=1
    for x in range(0,2**(repeatnum+1),3)[1:]:
            tap_tri *= x
    tri_in_cycle = [core_num*x for x in range(repeatnum+1)[1:]]
    
    tap_tri = (core_num*(1+len(tri_in_cycle)*tap_tri)+layers2comp*2*angular_chunks)
    tap = zeros(tap_tri, dtype=mesh.Mesh.dtype)
    #=============================================================
    #       CORE Creation
    theta = 0
    bfr = 0
    Ri = 0
    Re = radial_chnk_len
    delta_theta = 360/float(core_num)*(pi/180) # in radians
    for i in range(core_num):
        tap['vectors'][i+ bfr] = array([ [Re*cos(theta), Re*sin(theta), ch],
                                         [Ri*cos(theta), Ri*sin(theta), ch],
                                         [Re*cos(theta+delta_theta),
                                          Re*sin(theta+delta_theta), ch] ])
        theta+= delta_theta
    bfr  += core_num
    #=============================================================
    #       TRANSITION Creation
    for r in range(len(tri_in_cycle)):
        Ri = Re
        Re+= radial_chnk_len
        delta_theta/= 2
        for i in range(tri_in_cycle[r]):
            tap['vectors'][i*3+ bfr] = array([[Re*cos(theta), Re*sin(theta), ch],
                                            [Ri*cos(theta), Ri*sin(theta), ch],
                                            [Re*cos(theta+delta_theta),
                                             Re*sin(theta+delta_theta), ch] ])
            tap['vectors'][i*3+1+ bfr] = array([[Ri*cos(theta), Ri*sin(theta), ch],
                                            [Ri*cos(theta+2*delta_theta),
                                             Ri*sin(theta+2*delta_theta), ch],
                                            [Re*cos(theta+delta_theta),
                                             Re*sin(theta+delta_theta), ch]])
            tap['vectors'][i*3+2+bfr] = array([[Re*cos(theta+delta_theta),
                                                Re*sin(theta+delta_theta), ch],
                                            [Ri*cos(theta+2*delta_theta),
                                             Ri*sin(theta+2*delta_theta), ch],
                                            [Re*cos(theta+2*delta_theta),
                                             Re*sin(theta+2*delta_theta), ch] ])
            theta+= 2*delta_theta
        bfr  += tri_in_cycle[r]*3
    #=============================================================
    #       OUTER SHELL Creation
    if flag_2cover:
        radial_chnk_len = r2cover/float(layers2comp)
    
    for r in range(layers2comp):
        Ri = Re
        Re+= radial_chnk_len
        theta-= delta_theta/2
        for i in range(angular_chunks):
            tap['vectors'][i*2 + bfr] = array([[Re*cos(theta), Re*sin(theta), ch],
                                               [Ri*cos(theta+delta_theta/2),
                                                Ri*sin(theta+delta_theta/2), ch],
                                               [Re*cos(theta+delta_theta),
                                                Re*sin(theta+delta_theta), ch]])
            theta+= delta_theta/2
            tap['vectors'][i*2+1 + bfr] = array([[Ri*cos(theta), Ri*sin(theta), ch],
                                                 [Re*cos(theta+delta_theta/2),
                                                  Re*sin(theta+delta_theta/2), ch],
                                                 [Ri*cos(theta+delta_theta),
                                                  Ri*sin(theta+delta_theta), ch]])
            theta+= delta_theta/2
        bfr += 2*angular_chunks
        
    return tap

def build_pipemesh(radius, height, height_chunks, radial_chunks, theta=0):
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

def meshrender(mesh_list, index=-1):
    
    from matplotlib import pyplot
    from mpl_toolkits import mplot3d
    
    # Creating the plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    
    # Rendering
    if index==-1:
        for me in range(len(mesh_list)):
            axes.add_collection3d( mplot3d.art3d.Poly3DCollection( mesh_list[ me].vectors))
        scale = concatenate([me.points for me in mesh_list]).flatten(-1)
    else:
        axes.add_collection3d( mplot3d.art3d.Poly3DCollection( mesh_list[ index].vectors))
        scale = mesh_list[ index].points.flatten(-1)
    
    axes.auto_scale_xyz(scale, scale, scale)
    pyplot.show()

def meshlist2stl(mesh_list):
    
    justonemesh = mesh.Mesh( concatenate( [me.data for me in mesh_list]))
    justonemesh.save('mesh_X_try.stl', mode= stl.Mode.ASCII)
    

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
    
    #====================================================================
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
            #meshlist2stl( meshes)
            meshrender( meshes)
        else:
            P = 2*pi*radius
            angular_chunk_qty, core_qty = finishing2size( finish)
            
            ratio = height/P
            hgt_chunk_qty = int( angular_chunk_qty*ratio)
            
            if selector:
                onemesh = buid_circlemesh(radius, angular_chunk_qty, core_qty)
            else:
                onemesh = build_pipemesh(radius, height, hgt_chunk_qty, angular_chunk_qty)
                
            meshes = [mesh.Mesh(onemesh)]
            meshrender( meshes,0)

            
