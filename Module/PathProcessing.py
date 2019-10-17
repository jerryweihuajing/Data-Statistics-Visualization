# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 20:42:32 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Path Processing
"""

import os

#------------------------------------------------------------------------------
"""
Determines and creates a folder under a path

Args:
    path: path to be preprocessed

Returns:
    None
"""
def GenerateFolder(path):

    #remove first space
    path=path.strip()
    
    #remove tail \ sign
    path=path.rstrip("\\")
 
    #determine if the path exists (True/False)
    Exist=os.path.exists(path)
 
    #determine the results
    if not Exist:
        
        #Create directory operation function: creates a directory if it does not exist 
        os.makedirs(path)