# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 22:13:09 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Pc calculation
"""
'''
description: The utility model relates to an electronic calculation method for determining early consolidation pressure Pc

steps:
1 discrete points with unequal spacing, interpolating appropriate nearby values (Lagrange)
2 Calculate radius of curvature according to Angle bisector
3 calculate Pc and Cc according to appropriate curvature radius

INPUT：e,P,M
OUTPUT：Pc,Cc
'''

import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from scipy.linalg import solve

import operation_visualization as O_V
import calculation_numerical_analysis as C_N_A

#------------------------------------------------------------------------------
"""
Calculated radius of curvature

Args:
    which_3_points: 3 points to calculate
    
Returns:
    curvate radius
"""
def Curvature(which_3_points,show=False):
    
    #First, make sure that the x-coordinate of these three points increases
    x_sample=[this_x_y[0] for this_x_y in which_3_points]
    y_sample=[this_x_y[1] for this_x_y in which_3_points]
    
    #Establish correspondence
    map_x_y_sample=dict(zip(x_sample,y_sample))
    
    #Sorting oh
    x_sample.sort()
    
    new_x_sample=cp.deepcopy(x_sample)
    new_y_sample=[map_x_y_sample[this_x] for this_x in new_x_sample]
    
    #New 3 point list
    if len(which_3_points)==2:
        
        new_3_points=[which_3_points[0],
                      [0.4*which_3_points[0][0]+0.6*which_3_points[1][0],0.4*which_3_points[0][1]+0.6*which_3_points[1][1]],
                      which_3_points[1]]
        
    else:
        
        new_3_points=[[new_x_sample[k],new_y_sample[k]] for k in range(len(which_3_points))]

#    print(new_3_points)
#    print(which_3_points)   
    
    #Vector form is more convenient
    pos_A,pos_B,pos_C=np.array(new_3_points)
    
#    print(A,B,C)
    
    #The midpoint of AB is D, and the midpoint of BC is E
    pos_D=(pos_A+pos_B)/2
    pos_E=(pos_C+pos_B)/2
    
    #The slope of AB, the slope of BC
    k_AB=(pos_B-pos_A)[1]/(pos_B-pos_A)[0]
    k_BC=(pos_C-pos_B)[1]/(pos_C-pos_B)[0]
    
    #Vertical slope
    k_OD=-1/k_AB
    k_OE=-1/k_BC
    
    #OD的直线方程：y-y_D=k_OD*(x-x_D)
    #OE的直线方程：y-y_E=k_OE*(x-x_E)
    
    #便准化：
    #y-k_OD*x+(k_OD*x_D-y_D)
    #y-k_OE*x+(k_OE*x_D-y_E)
    
    #建立系数矩阵
    #|1 -k_OD| (y_D-k_OD*x_D)
    #|1 -k_OE| (y_E-k_OE*x_D)
    
    #Solve a binary first order equation
    A=np.array([[k_OD,-1],[k_OE,-1]])  
    B=np.array([k_OD*pos_D[0]-pos_D[1],k_OE*pos_E[0]-pos_E[1]])
      
    #Center coordinates
    pos_O=C_N_A.JacobiRoot(A,B)
    
#    print(pos_O)
    
#    #计算点到直线的距离加以验证
#    #AB的直线方程：y-y_D=k_AB*(x-x_D)
#    #BC的直线方程：y-y_E=k_BC*(x-x_E)
#    #D
#    A_D=1
#    B_D=-k_AB
#    C_D=(k_AB*pos_D[0]-pos_D[1])
#    
#    #E
#    A_E=1
#    B_E=-k_BC
#    C_E=(k_BC*pos_E[0]-pos_E[1])
#    
#    #计算距离
#    distance_D=abs(A_D*pos_O[0]+B_D*pos_O[1]+C_D)/np.sqrt(A_D**2+B_D**2)
#    distance_E=abs(A_E*pos_O[0]+B_E*pos_O[1]+C_E)/np.sqrt(A_E**2+B_E**2)
    
    distance_D=C_N_A.Distance(pos_O,pos_D)
    distance_E=C_N_A.Distance(pos_O,pos_E)
    
#    print(distance_D,distance_E)
    
    #show or not
    if show:
    
        #ABC
        for this_pos in new_3_points:
            
            plt.scatter(this_pos[0],this_pos[1],color='c')
        
        plt.scatter(pos_D[0],pos_D[1],color='y') #D
        plt.scatter(pos_E[0],pos_E[1],color='y') #E
        
        O_V.LinePlot(pos_D,k_AB,1,'k','center') #AB
        O_V.LinePlot(pos_E,k_BC,1,'k','center') #BC   
        
        O_V.LinePlot(pos_D,k_OD,distance_D+1,'k','end') #OD        
        O_V.LinePlot(pos_E,k_OE,distance_E+1,'k','end') #OE
        
    if np.round(distance_D)-np.round(distance_E)<0.1:

        return C_N_A.Distance(pos_O,pos_D),pos_O
    
    else:
    
        print('ERROR:Incorrect distance')
        
#------------------------------------------------------------------------------
"""
Calculate the minimum radius of curvature

Args:
    which_x_y: input data
    which_M: (defualt: 10)
    
Returns:
    None
"""
def MinCurvateRadius(which_x_y):

    '''default: (1/3, 3/4), (1/3, 2/4), (1/4, 2/4)'''
    #Calculate the radius of curvature
    base=int(len(which_x_y)/4)
    threshold=int(2*len(which_x_y)/4)
    
    #A list of radius of curvature
    curvate_radius=[]
    
    #Base overlay flag
#    base_plus=True
    
    for k in range(base,threshold):
        
#        print(which_x_y[k1:k+3])
           
        #The radius of curvature of this iteration
        that_R=Curvature(which_x_y[k:k+3])
        
        if that_R is None:
            
            continue
        
        curvate_radius.append(that_R[0])
        
#        if base_plus:
#            
#            base+=1
#        
#    #    print(that_R)
#        
#        if that_R>which_M:
#            
#            #The point of the minimum radius of curvature
#            curvate_radius.append(that_R)
#            
#            #Close the superposition
#            base_plus=False
            
#    if curvate_radius==[]:
#        
#        return base_plus
#    
    #Minimum radius of curvature
    R_min=min(curvate_radius)
#   
#    #Index of the minimum radius of curvature point
#    R_min_index=curvate_radius.index(R_min)+base  
    
    return curvate_radius.index(R_min)+base

#------------------------------------------------------------------------------
"""
Calculate the final result

Args:
    x: x input data
    y: y input data
    show: whether to plot the figure
    
Returns:
    None
"""
def CalculatePcAndCc(x,y,show=False):
    
    #result of interpolation
    new_x_y=C_N_A.LargrangeInterpolation(x,y)
    
    new_x=[this_x_y[0] for this_x_y in new_x_y]
    new_y=[this_x_y[1] for this_x_y in new_x_y]
    
    #Index of the minimum radius of curvature point
    R_min_index=MinCurvateRadius(new_x_y)
    
#    print(R_min_index)
    
    #Get the maximum curvature point (minimum radius of curvature)
    pos_P=new_x_y[R_min_index]   
    
    #plt.figure()
    #plt.plot(curvate_radius)
    
    #The slope of the tangent line at that point
    pos_O=Curvature(new_x_y[R_min_index:R_min_index+3])[1]
    
#    print(pos_O)
    
    #k_PD=-1/k_OP
    k_OP=(pos_P-pos_O)[1]/(pos_P-pos_O)[0]
    k_PD=-1/k_OP
     
    #horizontal line
    k_PS=0
    
    #The acute Angle between PD and PS is alpha
    alpha=abs(np.arctan(k_PD))
    
    #The slope of Angle bisector PQ
    k_PQ=-np.tan(alpha/2)
     
    #Equation of line of Angle bisector PQ: y-y_p =k_PQ*(x-x_p)
    #The linear equation of # data sample terminal MN is: y-y_m =k_MN*(x-x_m)
#    pos_M=np.array([new_x[-6],new_y[-6]])
#    pos_N=np.array([new_x[-1],new_y[-1]])
#    
#    if pos_M[0]==pos_N[0] and pos_M[1]==pos_N[1]:
#        
#        print('equal')
#        
#        pos_M=np.array([x[-2],y[-2]])
#        pos_N=np.array([x[-1],y[-1]])
          
#    for index_800 in range(len(x)):
#
#        if abs(x[index_800]-np.log10(800))<=0.01:
#            
#            pos_M=np.array([x[index_800],y[index_800]])
#            
#            break
#        
##    print(index_800,len(x))
#    
#    if index_800==len(x)-1:
#        
#        pos_M=np.array([x[-2],y[-2]])
        
#    pos_M=np.array([x[-2],y[-2]])
#    pos_N=np.array([x[-1],y[-1]])
#
##    print(pos_M,pos_N)
#    
#    #The slope of MN
#    k_MN=(pos_M-pos_N)[1]/(pos_M-pos_N)[0]
    
    pos_N=np.array([new_x[-1],new_y[-1]])
    
    #minimum of inclination above the curve
    k_list=[]
    
    for this_index in range(len(x)-1):
        
        this_start=np.array([x[this_index],y[this_index]])
        
#        print(this_start,pos_N)
        
        k_list.append((this_start-pos_N)[1]/(this_start-pos_N)[0])

    pos_M=np.array([x[k_list.index(min(k_list))],
                    y[k_list.index(min(k_list))]])
            
#    print(k_list.index(min(k_list)))
#    print(k_list)
    
    #The slope of MN
    k_MN=(pos_M-pos_N)[1]/(pos_M-pos_N)[0]
    
    #标准化：
    #y-k_PQ*x+(k_PQ*x_P-y_P)
    #y-k_MN*x+(k_OM*x_D-y_N)
    
    #建立系数矩阵
    #|1 -k_PQ| (y_P-k_PQ*x_P)
    #|1 -k_MN| (y_M-k_MN*x_M)
    
    #Solve a binary first order equation
    A=np.array([[1,-k_PQ],[1,-k_MN]])  
    B=np.array([pos_P[1]-k_PQ*pos_P[0],pos_M[1]-k_MN*pos_M[0]])
    
#    print(A,B)
    
    #Computing intersection
    Pc=10**solve(A,B)[1]
#    Cc=k_MN
    
    '''coordinate of point Q'''
    pos_Q=[solve(A,B)[1],solve(A,B)[0]]
    
    '''len_PQ'''
    len_PQ=C_N_A.Distance(pos_P,pos_Q)
    
    '''len_MN'''
    len_NQ=C_N_A.Distance(pos_N,pos_Q)
    
#    print('Cc=%.3f'%Cc)
#    print('Pc=%.3f'%Pc)
    
    #annotation font
    annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=16)
     
    #step stands for grid length
    x_step=(max(x)-min(x))/10
    y_step=(max(y)-min(y))/10
    
    #show or not
    if show:
               
        #dicide text position
        pos_text=(pos_Q[0]+2*x_step,pos_Q[1]-0*y_step)
            
        plt.annotate('Pc=%dkPa'%int(Pc),
                     xy=(pos_Q[0],pos_Q[1]),
                     xytext=pos_text,
                     weight='bold',color='k',
                     arrowprops=dict(arrowstyle='-|>',
                     connectionstyle='arc3',color='k'),
                     bbox=dict(boxstyle='round,pad=0.6', fc='grey', ec='k',lw=1 ,alpha=0.4),
                     fontproperties=annotation_font)
                     
        '''point O error!'''
#        plt.scatter(pos_O[0],pos_O[1],color='g')
#        plt.scatter(pos_P[0],pos_P[1],color='r')
           
#        LinePlot(pos_P,k_OP,0.2,'k','center') #OP        
        O_V.LinePlot(pos_P,k_PS,len_PQ*1.5,'k','start') #PS
        O_V.LinePlot(pos_P,k_PD,len_PQ*1.5,'k','start') #PD
        O_V.LinePlot(pos_P,k_PQ,len_PQ*1.5,'k','start') #PQ
        O_V.LinePlot(pos_N,k_MN,len_NQ*1.2,'k','end') #MN
        
        plt.scatter(pos_Q[0],pos_Q[1],color='grey')
        
    return Pc
     