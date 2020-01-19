# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 20:20:50 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-List Operation
"""

import numpy as np

from o_sample import sample

#------------------------------------------------------------------------------        
"""
Gets the new list based on the index list  

Args:
    which_list: list to be processed
    index_list: list of index which is valid

Returns:
    list based on the index list
"""          
def CustomIndexList(which_list,index_list):
    
    return [which_list[this_index] for this_index in index_list]

#------------------------------------------------------------------------------   
"""
Gets the new list based on the set of index list

Args:
    which_list: list to be processed

Returns:
    list based on the set of index list
"""          
def ValidIndexList(which_list):
    
    #result list
    ix_valid=[]
    
    #their names
    index_valid=[]
        
    #count invalid index
    repetition=0
    R=0
    NaN=0
    
    for ix in range(len(which_list)):
        
        this_index=which_list[ix]

        if this_index in index_valid:
            
            repetition+=1
            
            continue
        
        if isinstance(this_index,float):
            
            if np.isnan(this_index):
                
                NaN+=1
                
                continue
            
        if 'R' in this_index:
            
            R+=1
            
            continue
            
        ix_valid.append(ix)
        index_valid.append(this_index)
    
    return ix_valid

#------------------------------------------------------------------------------   
"""
Delete only duplicates

Args:
    which_list: list to be processed

Returns:
    index list
"""          
def ListWithoutRepetition(which_list):
    
    #result list
    ix_valid=[]
    
    #their names
    index_valid=[]
        
    #count invalid index
    repetition=0
    
    for ix in range(len(which_list)):
        
        this_index=which_list[ix]
        
        if this_index in index_valid:
            
            repetition+=1
            
            continue
                   
        ix_valid.append(ix)
        index_valid.append(this_index)
    
    return ix_valid

#------------------------------------------------------------------------------   
"""
Keep id with R

Args:
    which_list: list to be processed

Returns:
    list with 'R'
"""          
def ListWithR(which_list):

    return [ix for ix in range(len(which_list)) if 'R' in which_list[ix]]

#------------------------------------------------------------------------------   
"""
Filter cohesive silt to index list

Args:
    which_list: GB list to be processed

Returns:
    new index list
"""          
def GBIndexCohesiveSilt(which_list):
    
    ix_valid=[]
    
    for ix in range(len(which_list)):
        
        if not isinstance(which_list[ix],str):
            
            continue
        
        if '黏土' in which_list[ix]:

            ix_valid.append(ix)
        
    return ix_valid

#------------------------------------------------------------------------------   
"""
Filter floury soil to index list

Args:
    which_list: GB list to be processed

Returns:
    new index list
"""          
def GBIndexFlourySoil(which_list):
    
    ix_valid=[]
    
    for ix in range(len(which_list)):

        if not isinstance(which_list[ix],str):
            
            continue
        
        if '粉土' in which_list[ix]:

            ix_valid.append(ix)
        
    return ix_valid

#------------------------------------------------------------------------------   
"""
Filter for grain partition

Args:
    which_list: GB list to be processed

Returns:
    new index list
"""          
def GBIndexPartition(which_list):
    
    ix_valid=[]
    
    for ix in range(len(which_list)):

        if not isinstance(which_list[ix],str):
            
            continue
        
        if '砂' or '砾' in which_list[ix]:
            
            ix_valid.append(ix)
        
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

#------------------------------------------------------------------------------   
"""
Calculate the intersection between A and B

Args:
    set_A: list A
    set_B: list B

Returns:
    intersection list between A and B
""" 
def SetIntersection(set_A,set_B):
    
    set_intersection=[]
    
    for item in set_A:
        
        if item in set_B:
            
            set_intersection.append(item)
            
    return set_intersection

#------------------------------------------------------------------------------   
"""
Delete blank list in a list

Args:
    which_list: list consisting of list

Returns:
    intersection list between A and B
"""  
def DeleteBlankList(which_list):

    return [which_list.index(item) for item in which_list if item!=[]]

#------------------------------------------------------------------------------        
"""
Delete nan in a list and return a index list

Args:
    which_array: array to be processed

Returns:
    valid list
""" 
def ExpireNanIndexList(which_array):
    
    valid_index=[]
    
    #List form
    which_list=list(which_array)
    
    this_index=0
    
    for item in which_list:
        
        if not np.isnan(item):
            
            valid_index.append(this_index)
            
        this_index+=1
        
    return valid_index

#------------------------------------------------------------------------------
"""
Construct list of sample object

Args:
    list_pos_x: x coordinate list of samples to be constructed
    list_pos_y: y coordinate list of samples to be constructed
    
Returns:
    list of sample objects
"""    
def SampleList(list_pos_x,list_pos_y):
    
    samples=[]
    
    for k in range(len(list_pos_x)):
        
        that_sample=sample()
        
        that_sample.pos_x=list_pos_x[k]
        that_sample.pos_y=list_pos_y[k]
        
        samples.append(that_sample)
        
    return samples