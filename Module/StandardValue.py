# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 19:18:54 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Standard Value
"""

import numpy as np

def Average(data):
    
    return np.mean(data)

def StandardDeviation(data):
    
    square_of_sum=Average(data)**2
    
    n=len(data)
    
    return np.sqrt(np.sum([item**2-square_of_sum/n for item in data])/(n-1))

#r: correlation coefficient
def VariableCoefficient(data,r=0):
    
    return np.sqrt(1-r**2)*StandardDeviation(data)/Average(data)

def StatisticalCorrectionFactor(data,mode):
    
    n=len(data)
    
    operator=(1.704/np.sqrt(n)+4.678/np.square(n))*VariableCoefficient(data)
    
    if mode=='+':
        
        return 1+operator
    
    
    if mode=='-':
        
        return 1-operator
           
data=[1,2]

a=StatisticalCorrectionFactor(data,'+')