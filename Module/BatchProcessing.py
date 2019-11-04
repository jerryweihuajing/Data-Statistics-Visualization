# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:38:52 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Batch Processing
"""

import os

import ExcelStatistics as ES
import SiltClassification as SC

#------------------------------------------------------------------------------
"""
Make statistics from all sheets in all excel in folder path

Args:
    folder_path
    num_head_rows: top rows
    num_head_columns: left columns
    
Returns:
    None
"""
def Go(folder_path,num_head_rows,num_head_columns):
    
    for this_xls_name in os.listdir(folder_path):
        
        #create name of single path
        this_xls_path=folder_path+this_xls_name
      
        ES.WorkbookStatistics(this_xls_path,3,2)    
        SC.WorkbookClassification(this_xls_path,3,2)  