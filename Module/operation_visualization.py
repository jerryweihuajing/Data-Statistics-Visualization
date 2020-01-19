# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:28:15 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Visualization
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

import calculation_numerical_analysis as C_N_A

#------------------------------------------------------------------------------
"""
Make resilience curve

Args:
    x: x coordinates
    y: y coordinates
    x_step: step length of x
    y_step: step length of y
    annotation: (bool) whether to add annotation (default: False)

Returns:
    None
"""
def DataVisualization(x,y,x_step,y_step,annotation=True):
    
    #sample data font
    sammple_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=9)

    #combine x y
    which_x_y=[[x[k],y[k]] for k in range(len(x))]
    
    #result of interpolation
    new_x_y=C_N_A.LargrangeInterpolation(x,y)
    
    new_x=[this_x_y[0] for this_x_y in new_x_y]
    new_y=[this_x_y[1] for this_x_y in new_x_y]
    
    #plot curve
    plt.plot(new_x,new_y,'grey')
    
    #plot sample data
    for kk in range(len(which_x_y)):
        
         plt.scatter(x[kk],y[kk],color='k')
         
         if annotation:
             
             plt.annotate('(%d,%.3f)'%(np.round(10**x[kk]),y[kk]),
                          xy=(x[kk],y[kk]),
                          xytext=(x[kk]-0.5*x_step,y[kk]-0.3*y_step),
                          color='k',
                          fontproperties=sammple_font)
             
#------------------------------------------------------------------------------
"""
Point-slope line drawing

Args:
    which_pos: key point coordinate
    which_k: slope
    length: length between points
    which_color: color of line
    point_mode: ['center', 'start', 'end'] (defualt: 'center')
    
Returns:
    None
"""
def LinePlot(which_pos,
             which_k,
             length,
             which_color='k',
             point_mode='center'):
    
    #Custom step size
    step=0.01
    
    #Calculation steps
    amount=int(np.ceil(length/(step*np.sqrt(which_k**2+1))))
    
#    print(amount)
    
    #to list
    which_pos=list(which_pos)
    
    #Point coordinates
    which_pos_x,which_pos_y=which_pos
    
    #Create a sequence based on the point type
    if point_mode is 'start':
   
        x_array=C_N_A.ArrayOfStartPoint(which_pos_x,amount,step)
        
    if point_mode is 'center':
   
        x_array=C_N_A.ArrayOfCenterPoint(which_pos_x,amount,step)
    
    if point_mode is 'end':
   
        x_array=C_N_A.ArrayOfEndPoint(which_pos_x,amount,step)
        
    #The range of coordinates of a point
    y_array=[which_k*(this_x-which_pos_x)+which_pos_y for this_x in x_array]
    
    plt.plot(x_array,y_array,color=which_color)