#!/usr/bin/python


#       circle builder

from sys import exit
from numpy import pi, zeros, array, cos, sin
from stl import mesh

def build(radius, finishing, info_flag = False):
    
    angular_chunk_qty, core_qty = finishing2size( finishing)
    circularmeshdata = _build(radius, angular_chunk_qty, core_qty)
    
    if info_flag:
        return circularmeshdata, angular_chunk_qty, core_qty
    else:
        return circularmeshdata

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

def _build(radius, angular_chunks, core_num, ch = 0):
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
