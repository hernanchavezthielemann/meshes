#!/usr/bin/python

from numpy import concatenate
from matplotlib import pyplot
from mpl_toolkits import mplot3d

def meshrender( mesh_list, index=-1):
    
    # Creating the plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D( figure)
    
    # Rendering
    if index==-1:
        
        for me in range(len( mesh_list)):
            axes.add_collection3d( mplot3d.art3d.Poly3DCollection( mesh_list[ me].vectors))
        scale = concatenate([me.points for me in mesh_list]).flatten(-1)
        
    else:
        axes.add_collection3d( mplot3d.art3d.Poly3DCollection( mesh_list[ index].vectors))
        scale = mesh_list[ index].points.flatten(-1)
    
    axes.auto_scale_xyz(scale, scale, scale)
    pyplot.show()
