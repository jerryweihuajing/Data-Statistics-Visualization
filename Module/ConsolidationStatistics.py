# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:22:25 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Consolidation Calculation
"""

import xlrd
import pandas as pd

import HeadColumns as HC
import PcCalculation as PC
import ListOperation as LO

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

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
            
    
xls_path=r'C:\魏华敬\GitHub\DataStatistics\Data\input\土工试验54个.xls'

num_head_rows,num_head_columns=3,2

#------------------------------------------------------------------------------        
"""
Calculate Pc external interface

Args:
    P: pressure
    e: void ratio

Returns:
    valid list
""" 
def CalculatePc(P,e):
    
    #delete the first element
    valid_P=P[1:]
    valid_e=e[1:]
    
    if valid_P==[] or valid_e==[]:
        
        return None
    
    valid_logP=[np.log10(item) for item in valid_P]
    
    if PC.CalculatePcAndCc(PC.PreProcess(valid_e,valid_logP))>max(P):
        
        return None
    
    return PC.CalculatePcAndCc(PC.PreProcess(valid_e,valid_logP))    

print('')
print('--Consolidation Statistics')

plt.style.use('ggplot')

#open the excel sheet to be operated on
#formatting_info: keep the header format
workbook=xlrd.open_workbook(xls_path,formatting_info=True)

#construct map between sheet names and head rows
list_sheet_names=list(workbook.sheet_names())
 
Pc_workbook=[]

#traverse all sheets
for this_sheet_name in list_sheet_names:

    print('')
    print('...')
    print('......')
    print('->sheet name:',this_sheet_name)
    print('')
    
    #Data Frame object
    channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
    
    final_head_columns,unit_list=HC.HeadColumnsGeneration(channel,num_head_rows)
    
    #print(final_head_columns)
    
    #all info of dataframe
    value_matrix=channel.values
      
    #fetch the id of P and e
    index_e=[]
    index_e_high=[]
    
    #pressure
    P=[]
    P_high=[]
    
    #delete the repetition
    index_valid=LO.ValidIndexList(value_matrix[num_head_rows:,1])
        
    for k in range(num_head_columns,np.shape(value_matrix)[1]):
        
        #title str
        title=final_head_columns[k] 
        
        if '各级压力下的孔隙比' in title and '高压固结' not in title:
            
            print(k,title)
#            print(title.strip().split(' ')[1])
            
            index_e.append(k)
            P.append(float(title.strip().split(' ')[1]))
            
        if '各级压力下的孔隙比' in title and '高压固结' in title:
            
            print(k,title)
#            print(title.strip().split(' ')[1])
            
            index_e_high.append(k)
            P_high.append(float(title.strip().split(' ')[1]))
            
    #matrix to contain grain partition proportion
    data_e=np.zeros((len(index_valid),len(index_e)))
    data_e_high=np.zeros((len(index_valid),len(index_e_high)))
        
    column=0
        
    for this_index in index_e:
        
        data_e[:,column]=LO.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid)
    
        column+=1
   
    column=0
    
    for this_index in index_e_high:
        
        data_e_high[:,column]=LO.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid)
    
        column+=1
        
    Pc_normal=[]
    
    #normal
    for i in range(np.shape(data_e)[0]):
        
        expire_nan_index_list=ExpireNanIndexList(data_e[i])
    
        this_e=LO.CustomIndexList(list(data_e[i]),expire_nan_index_list)
        this_P=LO.CustomIndexList(P,expire_nan_index_list)

        Pc_normal.append(CalculatePc(this_P,this_e))
        
    Pc_high_pressure=[]
    
    #high pressure
    for i in range(np.shape(data_e_high)[0]):
        
        expire_nan_index_list=ExpireNanIndexList(data_e_high[i])
    
        this_e=LO.CustomIndexList(list(data_e_high[i]),expire_nan_index_list)
        this_P=LO.CustomIndexList(P_high,expire_nan_index_list)
        
        Pc_high_pressure.append(CalculatePc(this_P,this_e))
        
    Pc_sheet=[]
    
    for j in range(len(index_valid)):
        
#        print(Pc_normal[j],Pc_high_pressure[j])
        
        if Pc_normal[j] is None and Pc_high_pressure[j] is None:
            
            continue
        
        if Pc_normal[j] is None:
            
            Pc_sheet.append(Pc_high_pressure[j])
            
        if Pc_high_pressure[j] is None:
            
            Pc_sheet.append(Pc_normal[j])
     
    Pc_workbook+=Pc_sheet
        
fig,ax=plt.subplots(figsize=(8,8))

group=np.linspace(min(Pc_workbook),max(Pc_workbook),20)

title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
label_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=13) 
        
#plot histogram
plt.hist(Pc_workbook, group, histtype='bar', rwidth=0.95)
 
plt.title('Pc频数分布直方图\n样本总量:'+str(int(len(Pc_workbook))),
          FontProperties=title_font)  

plt.xlabel('Pc(kPa)',FontProperties=label_font)

#construct output folder path
figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\统计\\图\\'
    
#list of frequency
frequency=[0]*(len(group)-1)

#mannual histogram
for this_valid_data in Pc_workbook:

    for g in range(len(group)-1):
        
        if group[g]<=this_valid_data<=group[g+1]:
            
            frequency[g]+=1
            
            break
 
ax.yaxis.set_major_locator(MultipleLocator(int(np.ceil((max(frequency)-min(frequency))/20))))

#set ticks
plt.tick_params(labelsize=15)
labels = ax.get_xticklabels() + ax.get_yticklabels()

#label fonts
for this_label in labels:
    
    this_label.set_fontname('Times New Roman')
    
plt.savefig(figures_output_folder+'Pc.png')
plt.close()