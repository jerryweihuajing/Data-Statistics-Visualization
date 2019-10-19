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

#save as
new_workbook.save(tables_output_folder+'统计结果.xls')

#construct map between sheet names and head rows
list_sheet_names=list(workbook.sheet_names())

#default
if list_num_head_columns==None:
    
    list_num_head_columns=[num_head_columns]*len(list_sheet_names)
    
map_sheet_names_num_head_columns=dict(zip(list_sheet_names,list_num_head_columns))    

##traverse all sheets
#for this_sheet_name in workbook.sheet_names():

this_sheet_name='1'

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
        
        list_e0=value_matrix[:,k]
        head_e0=this_head
        
        break   
        break
 
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
        
