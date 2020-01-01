# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:15:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Head Columns from Data Frame object
"""

'''
demand:
1 Nan in the head columns also needs to be processed
'''
import copy as cp

#------------------------------------------------------------------------------
"""
Eradicate invalid data in head columns

Args:
    head_columns: head to be preprocessed

Returns:
    new head columns list
"""
def HeadColumnsPreProcess(head_columns):
    
    new_head_columns=[]

    #init first element of head columns
    this_head=head_columns[0]
    
    for this_str in head_columns:
        
        #process unnamed data
        if 'Unnamed' in this_str:
    
            new_head_columns.append(this_head)
        
        else:
                
            #collect normal data
            new_head_columns.append(this_str)
            
            this_head=cp.deepcopy(this_str)   
            
    return new_head_columns

#------------------------------------------------------------------------------
"""
Generate final head columns

Args:
    which_channel: data frame object
    num_head_lines: amount of head lines in an channel

Returns:
    final head columns list, unit list
"""
def HeadColumnsGeneration(which_channel,num_head_lines):

    #head of head
    head_columns=[]
    
    for item in list(which_channel.columns):
        
        head_columns.append(item.replace('\n',''))
        
    #lines 0,1,2 consists of table head    
    list_head_columns=[HeadColumnsPreProcess(head_columns)]
    
    for k in range(num_head_lines-1):
        
        this_head_column=[]
        
        #Data Frame values return a matrix
        for item in list(which_channel.values[k]):
        
            this_head_column.append(item)
        
        list_head_columns.append(this_head_column)
        
    final_head_columns=[]
    
    for k in range(len(head_columns)):
            
        this_head=''
        
        for this_head_columns in list_head_columns:
            
            this_str=str(this_head_columns[k])
            
            #eliminate invalid data
            if 'nan' not in this_str and '--' not in this_str:
                
                this_head+=' '
                this_head+=this_str
                
        final_head_columns.append(this_head.replace('\n',''))

    #unit list temprorary
    temp_unit_list=list(which_channel.values[num_head_lines-1])
    
    #final result list
    unit_list=[]
    
    #init first element of unit list
    this_unit='--'
    
    for this_str in temp_unit_list:
        
        #process unnamed data
        if 'nan' in str(this_str):
    
            unit_list.append(this_unit)
            
        else:
            
            #collect normal data
            unit_list.append(this_str)
            
            this_unit=cp.deepcopy(this_str)  

    return final_head_columns,unit_list