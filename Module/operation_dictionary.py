# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:44:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Dictionary Operation
"""

#------------------------------------------------------------------------------
"""
The dictionary searches for key by value

Args:
    which_dictionary: the dictionary which will be searched
    which_value: target value
    
Returns:
    key for which is searched
"""
def DictKeyOfValue(dictionary,value):
    
    keys=list(dictionary.keys())
    values=list(dictionary.values())

    return keys[values.index(value)]

#------------------------------------------------------------------------------
"""
The dictionary slice operation like list

Args:
    which_dictionary: the dictionary which will be searched
    start_id: starting index
    end_id: ending index
    
Returns:
    sliced dictionary
"""
def DictSlice(which_dict,start_id,end_id):

    return {this_key:which_dict[this_key] for this_key in list(which_dict.keys())[start_id:end_id]}

#------------------------------------------------------------------------------
"""
The dictionary was sorted by the values

Args:
    which_dictionary: the dictionary which will be searched
    
Returns:
    sorted dictionary
"""
def DictSortByValues(which_dict):
    
    new_dict={}

    for this_value in sorted(list(which_dict.values())):
        
        new_dict[DictKeyOfValue(which_dict,this_value)]=this_value
        
    return new_dict