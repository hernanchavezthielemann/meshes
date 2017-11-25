#!/usr/bin/python

from stl import mesh
from numpy import zeros, array, floor

def build_from_length(length, finishing):
    
    pt1= [ 0, 0, 0]
    pt2= [ 0, length, 0]
    pt3= [ length, 0, 0]
    pt4= [ length, length, 0]
    
    return _build(pt1, pt2, pt3, pt4, finishing)

def build_from_diagonal( pt1, pt4, finishing):
    
    if pt1[2]==pt4[2]:
        pt2= [pt1[0]]+pt4[1:]
        pt3= [pt4[0]]+pt1[1:]
    elif pt1[0]==pt4[0]:
        pt2= pt1[:2]+[pt4[2]]
        pt3= pt4[:2]+[pt1[2]]
    elif pt1[0]==pt4[0]:
        pt2= pt1[:2]+[pt4[2]]
        pt3= pt4[:2]+[pt1[2]]
    else:
        pt2= [pt1[0]]+pt4[1:]
        pt3= [pt4[0]]+pt1[1:]
        
    return _build(pt1, pt2, pt3, pt4, finishing)

def finishing2size(num):
    
    c_list = []
    flag = False
    core = 0
    if num < 2:
        num = 2
        sqrs = 1
        flag = True
    n=0
    while not flag:
        n+=1
        c_list.append(2**n)
        if num <= (2**(n)):
            num = 2**n
            flag = True
            sqrs = n
        elif n>12:
            exit('Warning!! ceil reached')
        
    return num, sqrs
def _build(pt1, pt2, pt3, pt4, finishing):
    
    x_len = max(pt2[0], pt3[0], pt4[0]) - min(pt2[0], pt3[0], pt1[0])
    y_len = max(pt2[1], pt3[1], pt4[1]) - min(pt2[1], pt3[1], pt1[1])
    z_len = max(pt2[2], pt3[2], pt4[2]) - min(pt2[2], pt3[2], pt1[2])
    
    finishing, squares = finishing2size( finishing)
    
    sqr_num = 2**((squares-1)/2)
    sqr_type = squares%2
    data = zeros(2*finishing, dtype=mesh.Mesh.dtype)
    
    x_step_len =   x_len/float(sqr_num)
    y_step_len =   y_len/float(sqr_num)
    z_step_len =   z_len/float(sqr_num)
    
    buffer = 0
    v_x = 0
    v_y = 0
    v_z = 0
    if z_step_len==0:
        x_step_len_i = x_step_len
        z_step_len_i = z_step_len   #0
        y_step_len_i = 0
        x_step_len_e = 0
        y_step_len_e = y_step_len
        z_step_len_e = z_step_len   #0
        
    elif y_step_len==0:
        x_step_len_i = 0
        z_step_len_i = z_step_len
        y_step_len_i = y_step_len   #0
        x_step_len_e = x_step_len
        y_step_len_e = y_step_len   #0
        z_step_len_e = 0
        
    elif x_step_len==0:
        x_step_len_i = x_step_len   #0
        z_step_len_i = 0
        y_step_len_i = y_step_len
        x_step_len_e = x_step_len   #0
        y_step_len_e = 0
        z_step_len_e = z_step_len
        
    
    for i in range(sqr_num):
        for j in range(sqr_num):
            
            pt1= [ v_x, v_y, v_z]
            
            pt2= [ v_x, v_y + y_step_len, v_z + z_step_len_i]
            pt3= [ v_x + x_step_len, v_y, v_z + z_step_len_e]
            
            pt4= [ v_x + x_step_len, v_y + y_step_len, v_z+ z_step_len]
            
            if sqr_type:
                data['vectors'][j*2+ buffer] = array([ pt1, pt2, pt3])
                data['vectors'][j*2+ 1+ buffer] = array([ pt2, pt3, pt4])
            else:
                pt5=[v_x+ x_step_len/2, v_y+ y_step_len/2, v_z+ z_step_len/2]
                
                data['vectors'][j*4+buffer] = array([ pt1, pt2, pt5])
                data['vectors'][j*4+1+buffer] = array([ pt1, pt3, pt5])
                data['vectors'][j*4+2+buffer] = array([ pt5, pt2, pt4])
                data['vectors'][j*4+3+buffer] = array([ pt5, pt3, pt4])
                
            v_x+= x_step_len_i
            v_y+= y_step_len_i
            v_z+= z_step_len_i
        if x_step_len_i>0:
            v_x=0
        elif y_step_len_i>0:
            v_y=0
        elif z_step_len_i>0:
            v_z=0
        
        v_x+= x_step_len_e
        v_y+= y_step_len_e
        v_z+= z_step_len_e
        
        buffer+= sqr_num*(2*(2-sqr_type))
    
    return data
