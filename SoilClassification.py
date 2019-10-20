# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:57:48 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Soil Classification
"""

from __init__ import *

import xlrd

import copy as cp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xlutils.copy import copy
from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import HeadColumns as HC
import PathProcessing as PP

#------------------------------------------------------------------------------
"""
Classification from silt compactness list

Args:
    list_e0: silt compactness list
    num_head_rows: top rows

Returns:
    result of e0 classification
"""       
def SiltCompactnessClassification(list_e0,num_head_rows=0):
    
    #result of e0 classification
    classification_e0=[]
    
    for this_data in list_e0[num_head_rows:]:
        
        valid_data=float(this_data)
        
        if valid_data<0.75:
            
            classification_e0.append('密实')
        
        elif 0.75<=valid_data<=0.9:
            
            classification_e0.append('中密')
        
        elif valid_data>0.9:
            
            classification_e0.append('稍密')
            
        else:
            
            classification_e0.append('')
            
    return classification_e0

#------------------------------------------------------------------------------
"""
Classification from silt moisture list

Args:
    list_ω0: silt moisture list
    num_head_rows: top rows

Returns:
    result of ω0 classification
"""  
def SiltMoistureClassification(list_ω0,num_head_rows=0):
    
    #result of ω0 classification
    classification_ω0=[]
    
    for this_data in list_ω0[num_head_rows:]:
        
        valid_data=float(this_data)
        
        if valid_data<20:
            
            classification_ω0.append('稍湿')
        
        elif 20<=valid_data<=30:
            
            classification_ω0.append('湿')
        
        elif valid_data>30:
            
            classification_ω0.append('很湿')
            
        else:
            
            classification_ω0.append('')
            
    return classification_ω0

#------------------------------------------------------------------------------
"""
Classification from clayey silt state list

Args:
    list_IL: clayey silt state list
    num_head_rows: top rows

Returns:
    result of IL classification
"""  
def ClayeySiltStateClassification(list_IL,num_head_rows=0):
    
    #result of IL classification
    classification_IL=[]
    
    for this_data in list_IL[num_head_rows:]:
        
        valid_data=float(this_data)
        
        if valid_data<=0:
            
            classification_IL.append('坚硬')
        
        elif 0<valid_data<=0.25:
            
            classification_IL.append('硬塑')
            
        elif 0.25<valid_data<=0.75:
            
            classification_IL.append('可塑')
            
        elif 0.75<valid_data<=1:
            
            classification_IL.append('软塑')   
            
        elif valid_data>1:
            
            classification_IL.append('流塑')
            
        else:
            
            classification_IL.append('')
            
    return classification_IL

xls_path='.\Data\\input\\土工试验54个.xls'

num_head_columns=2
num_head_rows=3
list_num_head_columns=None

print('')
print('--Workbook Statistics')

plt.style.use('ggplot')

#open the excel sheet to be operated on
#formatting_info: keep the header format
workbook=xlrd.open_workbook(xls_path,formatting_info=True)

#copy former workbook
new_workbook=copy(workbook)
    
#construct output folder path
tables_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\'

#construct map between sheet names and head rows
list_sheet_names=list(workbook.sheet_names())

#default
if list_num_head_columns==None:
    
    list_num_head_columns=[num_head_columns]*len(list_sheet_names)
    
map_sheet_names_num_head_columns=dict(zip(list_sheet_names,list_num_head_columns))    

##traverse all sheets
#for this_sheet_name in workbook.sheet_names():

this_sheet_name='1'

#open a sheet
this_sheet=new_workbook.get_sheet(this_sheet_name) 

print('')
print('...')
print('......')
print('->sheet name:',this_sheet_name)
print('')

#construct output folder path
figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\Figures\\sheet '+this_sheet_name+'\\'

#generate output folder
PP.GenerateFolder(figures_output_folder)
PP.GenerateFolder(tables_output_folder)

#Data Frame object
channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)

final_head_columns,unit_list=HC.HeadColumnsGeneration(channel,num_head_rows)

#all info of dataframe
value_matrix=channel.values

#index of line where info starts
start_info_row=num_head_rows+1   
     
for k in range(len(final_head_columns)):
    
    this_head=final_head_columns[k]
    
    #search for pore ratio
    if 'e0' in this_head:
        
        list_e0=value_matrix[:,k]
        head_e0=this_head
     
    #search for moisture content
    if 'ω0' in this_head:
        
        list_ω0=value_matrix[:,k]
        head_ω0=this_head 
        
    #search for liquidity index
    if 'IL' in this_head:
        
        list_IL=value_matrix[:,k]
        head_IL=this_head
        
classification_ω0=SiltMoistureClassification(list_ω0,num_head_rows)
classification_e0=SiltCompactnessClassification(list_e0,num_head_rows)
classification_IL=ClayeySiltStateClassification(list_IL,num_head_rows)

#collect them into list
classification_list=[classification_ω0,classification_e0,classification_IL]
title_list=['粉土密实度分类','粉土湿度分类','黏性土状态分类']

#plus columns
num_columns_plus=0

#write table head
for this_title in title_list:
    
    num_columns_plus+=1
    
    this_sheet.write(num_head_rows,
                     np.shape(channel.values)[1]+num_columns_plus,
                     this_title)
    
#plus columns   
num_columns_plus=0   

#write classification result    
for this_classification in classification_list:
    
    num_columns_plus+=1
    
    for i in range(len(this_classification)):
          
        this_sheet.write(i+start_info_row,
                         np.shape(channel.values)[1]+num_columns_plus,
                         this_classification[i])      

#save as
new_workbook.save(tables_output_folder+'分类结果.xls')
        