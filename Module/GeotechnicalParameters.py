# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 19:18:54 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Vital Parameters in Geotchnics
"""

import numpy as np

#------------------------------------------------------------------------------
"""
Avearge value calculation

Args:
    data: data array
    
Returns:
    Avearge value
"""
def Average(data):
    
    return np.mean(data)

#------------------------------------------------------------------------------
"""
Standard deviation calculation

Args:
    data: data array
    
Returns:
    Standard deviation
"""
def StandardDeviation(data):
    
    n=len(data)
    
    A=np.sum([item**2 for item in data])
    
    B=np.sum(data)**2/n
    
    return np.sqrt((A-B)/(n-1))

#------------------------------------------------------------------------------
"""
Residual standard deviation calculation in Geotechnical Engineering

Args:
    data: data array
    r: correlation coefficient (default: 0)
    
Returns:
    Residual standard deviation
"""
def ResidualStandardDeviation(data,r=0):
    
    return np.sqrt(1-r**2)*StandardDeviation(data)
    
#------------------------------------------------------------------------------
"""
Variable coefficient calculation in Geotechnical Engineering

Args:
    data: data array
    r: correlation coefficient (default: 0)
    
Returns:
    Variable coefficient
"""
def VariableCoefficient(data,r=0):
    
    return ResidualStandardDeviation(data,r)/Average(data)

#------------------------------------------------------------------------------
"""
Statistical correction factor calculation in Geotechnical Engineering

Args:
    data: data array
    mode: '+' or '-' which depends (default: -)
    r: correlation coefficient (default: 0)
    
Returns:
    Statistical correction factor
"""
def StatisticalCorrectionFactor(data,mode='-',r=0):
    
    n=len(data)
    
    operator=(1.704/np.sqrt(n)+4.678/np.square(n))*VariableCoefficient(data,r)
    
    if mode=='+':
        
        return 1+operator

    if mode=='-':
        
        return 1-operator
    
#------------------------------------------------------------------------------
"""
Standard value calculation in Geotechnical Engineering

Args:
    data: data array
    mode: '+' or '-' which depends (default: -)
    r: correlation coefficient (default: 0)
    
Returns:
    Standard value
"""         
def StandardValue(data,mode='-',r=0):
    
    return Average(data)*StatisticalCorrectionFactor(data,mode,r)
