# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:23:06 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Numerical Calculation
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
"""
Solve multiple primary equations using Jacobi methods

Args:
    which_A: coefficient matrix
    which_b: coefficient array
    
Returns:
    solution of system of equation
"""
def JacobiRoot(which_A,which_b):
    
    #Vectorizarion
    np.array(which_A)
    np.array(which_b)
    
    #The calculation results
    x=[]
    
    #Jacobi0
    J_0=np.linalg.det(which_A)
    
    for k in range(len(which_A)):
        
        A_temp=cp.deepcopy(which_A)
    
        #The first column is replaced by b
        A_temp[:,k]=which_b
        
        #calculation results
        x.append(np.linalg.det(A_temp)/J_0)
        
    return np.array(x)

#------------------------------------------------------------------------------
"""
Interpolation Lagrange base function

Args:
    x_y_sample: sample data
    x_i: x coordinates
    x: x coordiante to calculate
    
Returns:
    Lagrange Interpolation base function
"""
def LargrangeBase(x_y_sample,x_i,x):
    
    #Lists of x and y respectively
    x_sample=[this_x_y[0] for this_x_y in x_y_sample]
    
    up_product=1
    down_product=1
    
    #x_i in x_sample
    for this_x in x_sample:
        
        if this_x==x_i:
            
            continue
        
        up_product*=(this_x-x)
        down_product*=(this_x-x_i)
        
    return up_product/down_product

#------------------------------------------------------------------------------
"""
Interpolation Lagrange value

Args:
    x_y_sample: sample data
    x: x coordiante to calculate
    
Returns:
    Lagrange Interpolation value
"""
def LargrangeValue(x_y_sample,x):
        
    #final result
    interpolation_result=0
    
    #A linear combination
    for this_x_y in x_y_sample:
        
        interpolation_result+=this_x_y[1]*LargrangeBase(x_y_sample,this_x_y[0],x)
    
    return interpolation_result

#------------------------------------------------------------------------------
"""
Distance between A and B

Args:
    pos_A: coordinate ot point A
    pos_B: coordinate ot point B
    
Returns:
    Lagrange Interpolation value
"""
def Distance(pos_A,pos_B):
    
    #Determine the data type of pos_A,pos_B, whatever, and convert it to np.array
    if type(pos_A) is not np.array:
       
        pos_A=np.array(pos_A)
    
    if type(pos_B) is not np.array:
       
        pos_B=np.array(pos_B)
  
    return np.sqrt(np.sum((pos_A-pos_B)**2))

#------------------------------------------------------------------------------
"""
Interpolation Lagrange

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    show: (bool) whether to show
    
Returns:
    Lagrange Interpolation value x y list
"""
def LargrangeInterpolation(X,Y,n_step=1000,show=False):
    
    x_y_sample=[[X[k],Y[k]] for k in range(len(X))]
    
    new_x=np.linspace(min(X),max(X),n_step)
    new_y=np.array([LargrangeValue(x_y_sample,this_x) for this_x in new_x])
    
    if show:
        
        plt.plot(new_x,new_y,'c')
        
    return [[new_x[k],new_y[k]] for k in range(n_step)]

#------------------------------------------------------------------------------
"""
Interpolation former being curvate and latter being linear

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    show: (bool) whether to show
    
Returns:
    Lagrange Interpolation value x y list
"""
def CurvateAndLinearInterpolation(X,Y,n_step=100,show=False):
    
    x_y_sample=[[X[k],Y[k]] for k in range(len(X))]
    
    total_x=np.linspace(min(X),max(X),n_step)
    total_y=np.array([LargrangeValue(x_y_sample,this_x) for this_x in total_x])
    
    #former part
    former_x=np.linspace(min(X),np.log10(800),n_step)
    former_y=np.array([LargrangeValue(x_y_sample,this_x) for this_x in former_x])
    
    if max(X)-np.log10(800)<=0.01:
        
        return [[former_x[k],former_y[k]] for k in range(len(former_x))]
    
    #latter part
    X_for_linear=[total_x[k] for k in range(len(total_x)) if total_x[k]>=np.log10(800)]
    Y_for_linear=[total_y[k] for k in range(len(total_x)) if total_x[k]>=np.log10(800)]
    
#    print(X_for_linear,Y_for_linear)
    
    params= np.polyfit(X_for_linear,Y_for_linear,1)
    
    latter_x=np.linspace(np.log10(800),max(X),n_step)
    latter_y=np.polyval(params,latter_x)
    
    #combine them
    new_x=list(former_x)+list(latter_x)
    new_y=list(former_y)+list(latter_y)

    if show:
        
        plt.plot(new_x,new_y,'c')
        
    return [[new_x[k],new_y[k]] for k in range(len(new_x))]

#------------------------------------------------------------------------------
"""
Data preprocessing

Args:
    which_e: porosity array
    which_P: pressure array
    
Returns:
    Lagrange Interpolation value
"""
def PreProcess(which_P,which_e,show=False):
    
    x=which_P
    y=which_e

    #length is dimension
    length=len(x)
    
    if length>=len(y):
        
        length=len(y)
        
    #combined as coordinates
    x_y=[[x[k],y[k]] for k in range(length)]

    new_x=np.linspace(min(x),max(x),20)
    
    #result of interpolation
    new_y=np.array([LargrangeValue(x_y,this_new_x) for this_new_x in new_x])
    
    if show:
        
        #plt.figure()
        
        plt.plot(new_x,new_y,'c')
    
    #new points after interpolation
    new_x_y=[[new_x[k],new_y[k]] for k in range(len(new_x))]    

    return new_x_y

#------------------------------------------------------------------------------
"""
Quadratic fitting

Args:
    X: X array
    Y: Y array
    n_step: amount of step
    show: (bool) whether to show
    
Returns:
    Parabola Fitting value
"""
def ParabolaFitting(X,Y,n_step=100,show=False):
  
    X.reverse()
    Y.reverse()
    
    params= np.polyfit(X,Y,2)
    
    x=np.linspace(min(X),max(X),n_step)
    
    y=np.polyval(params,x)
    
    new_x=list(x)
    new_y=list(y)
    
    if show:
                
        plt.plot(new_x,new_y,'c')

    return [[new_x[k],new_y[k]] for k in range(len(new_x))] 
        
#------------------------------------------------------------------------------
"""
A sequence whose step length is step

Args:
    which_value: value list
    amount: amount of points
    step: step length between points
    
Returns:
    sequence whose step length is step
"""
def ArrayOfCenterPoint(which_value,amount,step):
    
    return [which_value+(k-amount/2)*step for k in range(amount)]

#------------------------------------------------------------------------------
"""
A sequence starting from a point with step length as step

Args:
    which_value: value list
    amount: amount of points
    step: step length between points
    
Returns:
    sequence starting from a point with step length as step
"""
def ArrayOfStartPoint(which_value,amount,step):
    
    return [which_value+k*step for k in range(amount)]

#------------------------------------------------------------------------------
"""
A sequence with a certain point as the end point and the step length is step

Args:
    which_value: value list
    amount: amount of points
    step: step length between points
    
Returns:
    sequence with a certain point as the end point and the step length is step
"""
def ArrayOfEndPoint(which_value,amount,step):
    
    return [which_value-k*step for k in range(amount)]
