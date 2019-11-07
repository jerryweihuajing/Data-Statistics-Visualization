# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 20:20:50 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：List Operation
"""

#------------------------------------------------------------------------------        
"""
Gets the new list based on the index list  

Args:
    which_list: list to be processed
    index_list: list of index which is valid

Returns:
    None
"""          
def CustomIndexList(which_list,index_list):
    
    return [which_list[this_index] for this_index in index_list]

#------------------------------------------------------------------------------   
"""
Gets the new list based on the set of index list

Args:
    which_list: list to be processed

Returns:
    None
"""          
def ValidIndexList(which_list):
    
    #result list
    ix_valid=[]
    
    #their names
    index_valid=[]
        
    #count invalid index
    repetition=0
    R=0
    
    for ix in range(len(which_list)):
        
        this_index=which_list[ix]
        
        
        if this_index in index_valid:
            
            repetition+=1
            
            continue
        
        if 'R' in this_index:
            
            R+=1
            
            continue
            
        ix_valid.append(ix)
        index_valid.append(this_index)
    
    return ix_valid

#------------------------------------------------------------------------------   
"""
Calculate the difference between A and B

Args:
    set_A: list A
    set_B: list B

Returns:
    difference list between A and B
""" 
def SetDiffernece(set_A,set_B):
    
    set_difference=[]
    
    for item in set_A:
        
        if item not in set_B:
            
            set_difference.append(item)
            
    return set_difference