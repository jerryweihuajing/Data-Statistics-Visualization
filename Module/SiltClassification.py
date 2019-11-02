# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:57:48 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Silt Classification
"""

import xlrd
import xlwt

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

#------------------------------------------------------------------------------
"""
Classification result statistics figure

Args:
    map_title_classification: a map between title and classification result
    figures_output_folder: output folder of figures

Returns:
    None
"""  
def ClassificationStatistics(map_title_classification,figures_output_folder):
    
    for kk in range(len(map_title_classification)):
            
        data=list(map_title_classification.values())[kk]
        title=list(map_title_classification.keys())[kk]
        
        #expire nan
        valid_str=[this_data for this_data in data if isinstance(this_data,str) and this_data!='']
        
        #group in x axis
        str_group=list(set(valid_str))
        
        #list of str frequency
        str_frequency=[0]*(len(str_group))
              
        #construct a dictionary as vote machine
        map_str_frequency=dict((this_valid_str,valid_str.count(this_valid_str)) for this_valid_str in valid_str)
        
    #        print(map_str_frequency)
       
        #frequency list
        str_frequency=list(map_str_frequency.values())
        
        fig,ax=plt.subplots(figsize=(8,8))
        
        #plot histogram
        plt.bar(range(len(str_frequency)),str_frequency,tick_label=str_group)
        
        ax.yaxis.set_major_locator(MultipleLocator(int(np.ceil((max(str_frequency)-min(str_frequency))/20))))
        
        #set ticks
        plt.tick_params(labelsize=60/len(str_group))
        
        #y label fonts
        for this_label in ax.get_yticklabels():
            
            this_label.set_fontname('Times New Roman')
            
        #x label fonts
        for this_label in ax.get_xticklabels():
            
            this_label.set_fontname('SimHei')
            
        title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
        label_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=13)  
        
        plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_str))),
                  FontProperties=title_font)
        
        plt.xlabel(title,FontProperties=label_font)
        
        plt.savefig(figures_output_folder+title+'.png')
        plt.close()
        
#------------------------------------------------------------------------------
"""
Make statistics from all sheets in one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns
    list_num_head_columns: list of num_head_rows (default: None)
    
Returns:
    None
"""
def SheetsClassification(xls_path,num_head_rows,num_head_columns,list_num_head_columns=None):
    
    print('')
    print('--Sheets Classification')
    
    plt.style.use('ggplot')
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #copy former workbook
    new_workbook=copy(workbook)
        
    #construct output folder path
    tables_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\分类\\'
    
    #generate output folder
    PP.GenerateFolder(tables_output_folder)
    
    #save as
    new_workbook.save(tables_output_folder+'分类结果.xls')
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
    #default
    if list_num_head_columns==None:
        
        list_num_head_columns=[num_head_columns]*len(list_sheet_names)
        
    map_sheet_names_num_head_columns=dict(zip(list_sheet_names,list_num_head_columns))    
    
    title_list=['粉土密实度分类','粉土湿度分类','黏性土状态分类']
    
    #traverse all sheets
    for this_sheet_name in workbook.sheet_names():
    
        #open a sheet
        this_sheet=new_workbook.get_sheet(this_sheet_name) 
        
        print('')
        print('...')
        print('......')
        print('->sheet name:',this_sheet_name)
        
        #construct output folder path
        figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\分类\\图\\表 '+this_sheet_name+'\\'
        
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
                
                print('-->head:'+head_e0)
             
            #search for moisture content
            if 'ω0' in this_head:
                
                list_ω0=value_matrix[:,k]
                head_ω0=this_head 
                
                print('-->head:'+head_ω0)
                
            #search for liquidity index
            if 'IL' in this_head:
                
                list_IL=value_matrix[:,k]
                head_IL=this_head
                
                print('-->head:'+head_IL)
                
        #list of classification result
        classification_ω0=SiltMoistureClassification(list_ω0,num_head_rows)
        classification_e0=SiltCompactnessClassification(list_e0,num_head_rows)
        classification_IL=ClayeySiltStateClassification(list_IL,num_head_rows)
        
        #collect them into list
        classification_list=[classification_ω0,classification_e0,classification_IL]

        #plus columns
        num_columns_plus=map_sheet_names_num_head_columns[this_sheet_name]-num_head_columns
        
        #define the border style
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour=0x3A    
         
        style = xlwt.XFStyle()
        style.borders = borders 
        
        #write table head
        for this_title in title_list:
            
            num_columns_plus+=1
            
            this_sheet.write(num_head_rows,
                             np.shape(channel.values)[1]+num_columns_plus,
                             this_title,
                             style)
            
        #plus columns   
        num_columns_plus=map_sheet_names_num_head_columns[this_sheet_name]-num_head_columns  
        
        #write classification result    
        for this_classification in classification_list:
            
            num_columns_plus+=1
            
            for i in range(len(this_classification)):
                  
                this_sheet.write(i+start_info_row,
                                 np.shape(channel.values)[1]+num_columns_plus,
                                 this_classification[i],
                                 style)      
    
        #save as
        new_workbook.save(tables_output_folder+'分类结果.xls')
        
        #construct a map between title and classification result
        map_title_classification=dict(zip(title_list,classification_list))
        
        #statistics result figures of classification
        ClassificationStatistics(map_title_classification,figures_output_folder)
         
#------------------------------------------------------------------------------
"""
Make statistics from all sheets in one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns
    
Returns:
    None
"""
def WorkbookClassification(xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Workbook Classification')
    
    plt.style.use('ggplot')
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #construct output folder path
    tables_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\分类\\'
    
    #construct output folder path
    figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\分类\\图\\总表\\'
    
    #generate output folder
    PP.GenerateFolder(figures_output_folder)
    PP.GenerateFolder(tables_output_folder)    

    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
         
    title_list=['粉土密实度分类','粉土湿度分类','黏性土状态分类']
    
    #total dictionanry
    list_map=[]
    
    #traverse all sheets
    for this_sheet_name in list_sheet_names:
            
        print('')
        print('...')
        print('......')
        print('->sheet name:',this_sheet_name)
        
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
                
                print('-->head:'+head_e0)
             
            #search for moisture content
            if 'ω0' in this_head:
                
                list_ω0=value_matrix[:,k]
                head_ω0=this_head 
                
                print('-->head:'+head_ω0)
                
            #search for liquidity index
            if 'IL' in this_head:
                
                list_IL=value_matrix[:,k]
                head_IL=this_head
                
                print('-->head:'+head_IL)
                
        #list of classification result
        classification_ω0=SiltMoistureClassification(list_ω0,num_head_rows)
        classification_e0=SiltCompactnessClassification(list_e0,num_head_rows)
        classification_IL=ClayeySiltStateClassification(list_IL,num_head_rows)
        
        #collect them into list
        classification_list=[classification_ω0,classification_e0,classification_IL]

        #construct a map between title and classification result
        map_title_classification=dict(zip(title_list,classification_list))
        
        #collect this map
        list_map.append(map_title_classification)
    
    '''re classification'''
#    #total classification result map    
#    total_map_title_classification={}
#    
#    #initiate
#    for this_title in title_list:
#        
#        total_map_title_classification[this_title]=0
#      
#    #sum up
#    for this_map in list_map:
#        
#        for this_key in list(this_map.keys()):
#            
#            total_map_title_classification[this_key]+=this_map[this_key]
            
#    #statistics result figures of classification
#    ClassificationStatistics(total_map_title_classification,figures_output_folder)
        