# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:57:48 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Silt Classification
"""

import xlrd
import xlwt

import copy as cp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from xlutils.copy import copy
from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import operation_list as O_L
import operation_path as O_P
import operation_dictionary as O_D
import operation_head_column as O_H_C

from o_grain import grain

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
        
        if np.isnan(valid_data):
            
            continue
        
        if valid_data<0.75:
            
            classification_e0.append('密实')
        
        elif 0.75<=valid_data<=0.9:
            
            classification_e0.append('中密')
        
        elif valid_data>0.9:
            
            classification_e0.append('稍密')
            
        else:
            
            classification_e0.append('其他')
            
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
        
        if np.isnan(valid_data):
            
            continue
        
        if valid_data<20:
            
            classification_ω0.append('稍湿')
        
        elif 20<=valid_data<=30:
            
            classification_ω0.append('湿')
        
        elif valid_data>30:
            
            classification_ω0.append('很湿')
            
        else:
            
            classification_ω0.append('其他')
            
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
        
        if np.isnan(valid_data):
            
            continue
        
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
            
            classification_IL.append('其他')
            
    return classification_IL

#------------------------------------------------------------------------------
"""
Convert the list into a frequency distribution dictionary

Args:
    which_list: list to be processed 
    
Returns:
    result dictionary
"""  
def List2FrequencyMap(which_list):
    
    keys=list(set(which_list))
    
    #frequency distribution map
    map_frequency={}
    
    for this_key in keys:
        
        map_frequency[this_key]=which_list.count(this_key)    
    
    return map_frequency

#------------------------------------------------------------------------------
"""
Save title and class result  as table

Args:
    map_title_classification: map between title and classification result
    tables_output_folder: tables save folder
        
Returns:
    None
""" 
def TitleAndClassification2Table(map_title_classification,tables_output_folder):
    
    #delete blank list
    title_list=list(map_title_classification.keys())
    classification_list=list(map_title_classification.values())
    
    #frequency to save
    list_frequency_map=[List2FrequencyMap(classification_list[ix]) for ix in range(len(title_list))]
    
    #construct new workbook   
    new_workbook=xlwt.Workbook(encoding='utf-8') 
    
    #construct new sheet
    new_sheet=new_workbook.add_sheet("总表")          
          
    #define the border style
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour=0x3A    
     
    style = xlwt.XFStyle()
    style.borders = borders
    
    #instant row
    row=0
    
    #title
    for k in range(len(title_list)):
        
        new_sheet.write(row,0,title_list[k],style)
        
        row+=1
        
        new_sheet.write(row,0,'总量',style)
        new_sheet.write(row,1,len(classification_list[k]),style)
        
        row+=1
        
        
        for kk in range(len(list_frequency_map[k])):
            
            if isinstance(list(list_frequency_map[k].keys())[kk],str):
                
                new_sheet.write(row,0,list(list_frequency_map[k].keys())[kk],style)
                
            else:
                
                new_sheet.write(row,0,'其他',style)
                
            new_sheet.write(row,1,list(list_frequency_map[k].values())[kk],style)
            
            row+=1
            
        row+=1
            
    new_workbook.save(tables_output_folder+'统计总表.xls')

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
    
    plt.style.use('ggplot')
    
    for kk in range(len(map_title_classification)):
            
        data=list(map_title_classification.values())[kk]
        title=list(map_title_classification.keys())[kk]
        
        #expire nan
        valid_str=[this_data for this_data in data if isinstance(this_data,str) and this_data!='']
                   
        #construct a dictionary as vote machine
        map_str_frequency=O_D.DictSortByValues(dict((this_valid_str,valid_str.count(this_valid_str)) for this_valid_str in valid_str))

        #frequency list
        str_frequency=list(map_str_frequency.values())
        
        #group in x axis
        str_group=list(map_str_frequency.keys())
        
        #init
        list_str=cp.deepcopy(str_group)
        
        new_map_str_frequency={}
        
        if title=='粉土密实度分类':
            
            list_str=['稍密','中密','密实']
            
        if title=='粉土湿度分类':
            
            list_str=['湿','很湿']
            
        if title=='黏性土状态分类':
            
            list_str=['坚硬','硬塑','可塑','软塑','流塑']
            
        if title=='土的分类':
            
            list_str=['砾砂','粗砂','中砂','细砂','粉砂','粉土','粉质黏土','黏土','淤泥','淤泥质粉质黏土','淤泥质黏土']
            
        list_frequency=[map_str_frequency[this_str] for this_str in list_str]

        fig,ax=plt.subplots(figsize=(16,0.8*len(map_str_frequency)))

        #plot histogram
        plt.barh(range(len(list_str)),list_frequency,tick_label=list_str)

        if len(map_str_frequency)!=1:
            
            ax.xaxis.set_major_locator(MultipleLocator(int(np.ceil((max(str_frequency)-min(str_frequency))/20))))
    
        #set ticks
        plt.tick_params(labelsize=15)
        
        #y label fonts
        for this_label in ax.get_xticklabels():
            
            this_label.set_fontname('Times New Roman')
            
        #x label fonts
        for this_label in ax.get_yticklabels():
            
            this_label.set_fontname('SimHei')
            
        title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
        
        plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_str))),
                  FontProperties=title_font)
        
        fig_path=figures_output_folder+title+'.png'
        
        #save the fig
        plt.savefig(fig_path,dpi=300,bbox_inches='tight')
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
    O_P.GenerateFolder(tables_output_folder)
    
    #save as
    new_workbook.save(tables_output_folder+'分类结果.xls')
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
    #default
    if list_num_head_columns==None:
        
        list_num_head_columns=[num_head_columns]*len(list_sheet_names)
        
    map_sheet_names_num_head_columns=dict(zip(list_sheet_names,list_num_head_columns))    
    
    title_list=['粉土密实度分类',
                '粉土湿度分类',
                '黏性土状态分类',
                '土的分类',
                '备注']
    
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
        O_P.GenerateFolder(figures_output_folder)
        O_P.GenerateFolder(tables_output_folder)
        
        #Data Frame object
        channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
        
        final_head_columns,unit_list=O_H_C.HeadColumnsGeneration(channel,num_head_rows)
        
        #all info of dataframe
        value_matrix=channel.values
        
        #delete the repetition
        index_valid=O_L.ValidIndexList(value_matrix[num_head_rows:,1])
        
        #index of line where info starts
        start_info_row=num_head_rows+1   
             
        for k in range(len(final_head_columns)):
            
            this_head=final_head_columns[k]
            
            #search for note and make statistics
            if '备' in this_head or '注' in this_head:
                
                list_note=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_note=this_head
                
                print('-->head:'+head_note)
                
            #search for type of silt
            if '分类' in this_head:
                
                list_GB=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_GB=this_head
                
                print('-->head:'+head_GB)
                
            #search for pore ratio
            if 'e0' in this_head:
     
                list_e0=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_e0=this_head
                
                print('-->head:'+head_e0)
             
            #search for moisture content
            if 'ω0' in this_head:
                
                list_ω0=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_ω0=this_head 
                
                print('-->head:'+head_ω0)
                
            #search for liquidity index
            if 'IL' in this_head:
                
                list_IL=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_IL=this_head
                
                print('-->head:'+head_IL)
                
        #list of classification result
        classification_ω0=SiltMoistureClassification(list_ω0,num_head_rows)
        classification_e0=SiltCompactnessClassification(list_e0,num_head_rows)
        classification_IL=ClayeySiltStateClassification(list_IL,num_head_rows)
        classification_GB=cp.deepcopy(list_GB)
        classification_note=cp.deepcopy(list_note)
        
        #collect them into list
        classification_list=[classification_e0,
                             classification_ω0,
                             classification_IL,
                             classification_GB,
                             classification_note]
        #frequency to save
        list_frequency_map=[List2FrequencyMap(classification_list[ix]) for ix in range(len(title_list))]
        
        #construct new workbook   
        new_workbook=xlwt.Workbook(encoding='utf-8') 
        
        #construct new sheet
        new_sheet=new_workbook.add_sheet("总表")          
              
        #define the border style
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour=0x3A    
         
        style = xlwt.XFStyle()
        style.borders = borders
        
        #instant row
        row=0
        
        #title
        for k in range(len(title_list)):
            
            new_sheet.write(row,0,title_list[k],style)
            
            row+=1
            
            new_sheet.write(row,0,'总量',style)
            new_sheet.write(row,1,len(classification_list[k]),style)
            
            row+=1
            
#            print(list_frequency_map[k])
            
            for kk in range(len(list_frequency_map[k])):
                
                if isinstance(list(list_frequency_map[k].keys())[kk],str):
                    
                    new_sheet.write(row,0,list(list_frequency_map[k].keys())[kk],style)
                    
                else:
                    
                    new_sheet.write(row,0,'其他',style)
                    
                new_sheet.write(row,1,list(list_frequency_map[k].values())[kk],style)
                
                row+=1
                
            row+=1
                
        new_workbook.save(tables_output_folder+'统计总表.xls')
    
        #plus columns
        num_columns_plus=map_sheet_names_num_head_columns[this_sheet_name]-num_head_columns
        
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
        
        #delete blank list
        real_title_list=O_L.CustomIndexList(title_list,O_L.DeleteBlankList(classification_list))
        real_classification_list=O_L.CustomIndexList(classification_list,O_L.DeleteBlankList(classification_list))
        
        #delete nan in classification list
        new_classification_list=[]
        
        for this_classification in real_classification_list:
            
            new_classification=[]
        
            for item in this_classification:
                
                if not isinstance(item,str):
                    
                    if np.isnan(item):
                        
    #                    print('nan')
                        
                        continue
                    
                new_classification.append(item)
                
            new_classification_list.append(new_classification)
            
        #construct a map between title and classification result
        map_title_classification=dict(zip(real_title_list,new_classification_list))
        
        #statistics result tables of classification
        TitleAndClassification2Table(map_title_classification,tables_output_folder)
        
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
    figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\分类\\图\\总图\\'
    
    #generate output folder
    O_P.GenerateFolder(figures_output_folder)
  
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
         
    title_list=['粉土密实度分类',
                '粉土湿度分类',
                '黏性土状态分类',
                '土的分类',
                '备注']
    
    #classification result list
    classification_ω0=[]
    classification_e0=[]
    classification_IL=[]
    classification_GB=[]
    classification_note=[]
    
    #classification result list
    classification_ω0,classification_e0,classification_IL=[],[],[]
    
    #traverse all sheets
    for this_sheet_name in list_sheet_names[-1:]:
            
        print('')
        print('...')
        print('......')
        print('->sheet name:',this_sheet_name)
        
        #Data Frame object
        channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
        
        final_head_columns,unit_list=O_H_C.HeadColumnsGeneration(channel,num_head_rows)
        
        #all info of dataframe
        value_matrix=channel.values
        
        #delete the repetition
        index_valid=O_L.ValidIndexList(value_matrix[num_head_rows:,1])
        
        print('-->Valid Samples:',len(index_valid))
        
        for k in range(len(final_head_columns)):
            
            this_head=final_head_columns[k]
            
            #search for note and make statistics
            if '备' in this_head or '注' in this_head:
                
                list_note=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_note=this_head
                
                print('-->head:'+head_note)
                
            #search for type of silt
            if '分类' in this_head:
                
                list_GB=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_GB=this_head
                
                print('-->head:'+head_GB)
                
            #search for pore ratio
            if 'e0' in this_head:
     
                list_e0=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_e0=this_head
                
                print('-->head:'+head_e0)
             
            #search for moisture content
            if 'ω0' in this_head:
                
                list_ω0=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_ω0=this_head 
                
                print('-->head:'+head_ω0)
                
            #search for liquidity index
            if 'IL' in this_head:
                
                list_IL=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_IL=this_head
                
                print('-->head:'+head_IL)

        #filter floury soil
        index_floury_soil=O_L.GBIndexFlourySoil(list_GB)
        
        ω0_valid=O_L.CustomIndexList(list_ω0,index_floury_soil)
        e0_valid=O_L.CustomIndexList(list_e0,index_floury_soil)

        #filter cohesive silt
        index_cohesive_silt=O_L.GBIndexCohesiveSilt(list_GB)
        
        IL_valid=O_L.CustomIndexList(list_IL,index_cohesive_silt)
     
        #list of classification result
        #floury soil
        classification_ω0+=SiltMoistureClassification(ω0_valid,num_head_rows)
        classification_e0+=SiltCompactnessClassification(e0_valid,num_head_rows)
        
        #cohesive silt
        classification_IL+=ClayeySiltStateClassification(IL_valid,num_head_rows)
        
        #GB
        classification_GB+=list_GB
        
        #note
        classification_note+=list_note
        
    #collect them into list
    classification_list=[classification_e0,
                         classification_ω0,
                         classification_IL,
                         classification_GB,
                         classification_note]
    #frequency to save
    list_frequency_map=[List2FrequencyMap(classification_list[ix]) for ix in range(len(title_list))]
    
    #construct new workbook   
    new_workbook=xlwt.Workbook(encoding='utf-8') 
    
    #construct new sheet
    new_sheet=new_workbook.add_sheet("总表")          
          
    #define the border style
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour=0x3A    
     
    style = xlwt.XFStyle()
    style.borders = borders
    
    #instant row
    row=0
    
    #title
    for k in range(len(title_list)):
        
        new_sheet.write(row,0,title_list[k],style)
        
        row+=1
        
        new_sheet.write(row,0,'总量',style)
        new_sheet.write(row,1,len(classification_list[k]),style)
        
        row+=1
        
#        print(list_frequency_map[k])
        
        for kk in range(len(list_frequency_map[k])):
            
            if isinstance(list(list_frequency_map[k].keys())[kk],str):
                
                new_sheet.write(row,0,list(list_frequency_map[k].keys())[kk],style)
                
            else:
                
                new_sheet.write(row,0,'其他',style)
                
            new_sheet.write(row,1,list(list_frequency_map[k].values())[kk],style)
            
            row+=1
            
        row+=1
            
    new_workbook.save(tables_output_folder+'统计总表.xls')
    
    #delete blank list
    real_title_list=O_L.CustomIndexList(title_list,O_L.DeleteBlankList(classification_list))
    real_classification_list=O_L.CustomIndexList(classification_list,O_L.DeleteBlankList(classification_list))
    
    #delete nan in classification list
    new_classification_list=[]
    
    for this_classification in real_classification_list:
        
        new_classification=[]
    
        for item in this_classification:
            
            if not isinstance(item,str):
                
                if np.isnan(item):
                    
#                    print('nan')
                    
                    continue
                
            new_classification.append(item)
            
        new_classification_list.append(new_classification)
        
    #construct a map between title and classification result
    map_title_classification=dict(zip(real_title_list,new_classification_list))
    
    #statistics result tables of classification
    TitleAndClassification2Table(map_title_classification,tables_output_folder)
    
    #statistics result figures of classification
    ClassificationStatistics(map_title_classification,figures_output_folder)
    
#------------------------------------------------------------------------------
"""
Make statistics from all sheets in one excel

Args:
    list_xls_path: list path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns
    
Returns:
    None
"""
def MergedWorkbookClassification(list_xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Merged Workbook Classification')
    
    plt.style.use('ggplot')
    
    #construct output folder path
    tables_output_folder=list_xls_path[0].split('input')[0]+'output\\颗分汇总\\分类\\'
    figures_output_folder=list_xls_path[0].split('input')[0]+'output\\颗分汇总\\分类\\图\\总图\\'
        
    #generate output folder
    O_P.GenerateFolder(tables_output_folder)
    O_P.GenerateFolder(figures_output_folder)
    
    #DF channels
    total_channels=[]
    
    for this_xls_path in list_xls_path:
        
        #open the excel sheet to be operated on
        #formatting_info: keep the header format
        workbook=xlrd.open_workbook(this_xls_path,formatting_info=True)
        
        #construct map between sheet names and head rows
        list_sheet_names=list(workbook.sheet_names())
     
        #traverse all sheets
        for this_sheet_name in list_sheet_names:
            
            #Data Frame object
            that_channel=pd.read_excel(this_xls_path,sheet_name=this_sheet_name)
            
            #collect it
            total_channels.append(that_channel)
     
    title_list=['粉土密实度分类',
                '粉土湿度分类',
                '黏性土状态分类',
                '土的分类',
                '备注',
                '砂类土分类（代号）',
                '砾类土分类（代号）',
                '砂类土分类（名称）',
                '砾类土分类（名称）']
    
    #classification result list
    classification_ω0=[]
    classification_e0=[]
    classification_IL=[]
    classification_GB=[]
    classification_note=[]
    classification_S_type=[]
    classification_G_type=[]
    classification_S_code=[]
    classification_G_code=[]
    
    #traverse all sheets
    for channel in total_channels:
    
        print('')
        print('...')
        print('......')
        print('')

        final_head_columns,unit_list=O_H_C.HeadColumnsGeneration(channel,num_head_rows)
        
        #all info of dataframe
        value_matrix=channel.values
        
        #delete the repetition
        index_valid=O_L.ValidIndexList(value_matrix[num_head_rows:,1])
        
        print('-->Valid Samples:',len(index_valid))
        
        for k in range(len(final_head_columns)):
            
            this_head=final_head_columns[k]
            
            #search for note and make statistics
            if '备' in this_head or '注' in this_head:
                
                list_note=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_note=this_head
                
                print('-->head:'+head_note)
                
            #search for type of silt
            if '分类' in this_head:
                
                list_GB=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_GB=this_head
                
                print('-->head:'+head_GB)
                
            #search for pore ratio
            if 'e0' in this_head:
     
                list_e0=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_e0=this_head
                
                print('-->head:'+head_e0)
             
            #search for moisture content
            if 'ω0' in this_head:
                
                list_ω0=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_ω0=this_head 
                
                print('-->head:'+head_ω0)
                
            #search for liquidity index
            if 'IL' in this_head:
                
                list_IL=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                head_IL=this_head
                
                print('-->head:'+head_IL)
        
        #delete the repetition and remove label R
        index_valid=O_L.ListWithR(value_matrix[num_head_rows:,1])
     
        print('-->Total Samples:',len(value_matrix[num_head_rows:,1]))
        print('-->Valid Samples:',len(index_valid))
        
        #partition index list
        list_partition_index=[]
        
        for k in range(num_head_columns,np.shape(value_matrix)[1]):
    
            #title str
            title=final_head_columns[k]
            
    #        print(k,title)
        
            if '颗' and '粒' and '分' and '析' in title:
                
                print('-->',title)
                     
                list_partition_index.append(k)
            
            if '不' and '均' and '匀' in title:
                
                print('-->',title)
                
                data_Cu=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                
            if '曲' and '率' in title:
                
                print('-->',title)
                
                data_Ce=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
                
            if '分' and '类' in title:
                
                print('-->',title)
                
                data_GB=O_L.CustomIndexList(list(value_matrix[num_head_rows:,k]),index_valid)
            
    #    print(list_partition_index)
        
        #for partition
        index_partition=O_L.GBIndexPartition(data_GB)
         
        #matrix to contain grain partition proportion
        data_partition=np.zeros((len(index_partition),len(list_partition_index)))
        
        column=0
        
        for this_index in list_partition_index:
            
            data_partition[:,column]=O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_partition)
        
            column+=1
        
        #valid part
        GB_partition=O_L.CustomIndexList(data_GB,index_partition)
        Cu_partition=O_L.CustomIndexList(data_Cu,index_partition)
        Ce_partition=O_L.CustomIndexList(data_Ce,index_partition)
        
    #        len(index_valid)
        
        #classificaiotn result
        S_classification_type=[]
        G_classification_type=[]
        S_classification_code=[]
        G_classification_code=[]
        
        for kk in range(len(index_partition)):
                  
            #construct new object
            this_grain=grain()
            
            this_grain.silt_type=GB_partition[kk]
            this_grain.InitMap(list(data_partition[kk,:]))   
            
            this_grain.Partition()
            this_grain.Classification(Cu_partition[kk],Ce_partition[kk])
            
            if '砂' in this_grain.silt_type:
                
                S_classification_type.append(this_grain.classification_type)
                S_classification_code.append(this_grain.classification_code)
                
            if '砾' in this_grain.silt_type:
                
                G_classification_type.append(this_grain.classification_type)
                G_classification_code.append(this_grain.classification_code)
            
        #filter floury soil
        index_floury_soil=O_L.GBIndexFlourySoil(list_GB)

        ω0_valid=O_L.CustomIndexList(list_ω0,index_floury_soil)
        e0_valid=O_L.CustomIndexList(list_e0,index_floury_soil)

        #filter cohesive silt
        index_cohesive_silt=O_L.GBIndexCohesiveSilt(list_GB)

        IL_valid=O_L.CustomIndexList(list_IL,index_cohesive_silt)
     
        #list of classification result
        #floury soil
        classification_ω0+=SiltMoistureClassification(ω0_valid,num_head_rows)
        classification_e0+=SiltCompactnessClassification(e0_valid,num_head_rows)
        
        #cohesive silt
        classification_IL+=ClayeySiltStateClassification(IL_valid,num_head_rows)
        
        #GB
        classification_GB+=list_GB
        
        #note
        classification_note+=list_note
        
#        print(len(classification_GB),len(classification_note))
        
        #grain partition result
        classification_S_type+=S_classification_type
        classification_G_type+=G_classification_type
        classification_S_code+=S_classification_code
        classification_G_code+=G_classification_code
        
    #collect them into list
    classification_list=[classification_e0,
                         classification_ω0,
                         classification_IL,
                         classification_GB,
                         classification_note,
                         classification_S_type,
                         classification_G_type,
                         classification_S_code,
                         classification_G_code]
        
    #delete blank list
    real_title_list=O_L.CustomIndexList(title_list,O_L.DeleteBlankList(classification_list))
    real_classification_list=O_L.CustomIndexList(classification_list,O_L.DeleteBlankList(classification_list))
    
    #delete nan in classification list
    new_classification_list=[]
    
    for this_classification in real_classification_list:
        
        new_classification=[]
    
        for item in this_classification:
            
            if not isinstance(item,str):
                
                if np.isnan(item):
                    
#                    print('nan')
                    
                    continue
                
            new_classification.append(item)
            
        new_classification_list.append(new_classification)
        
    #construct a map between title and classification result
    map_title_classification=dict(zip(real_title_list,new_classification_list))
    
    #statistics result tables of classification
    TitleAndClassification2Table(map_title_classification,tables_output_folder)
    
    #statistics result figures of classification
    ClassificationStatistics(map_title_classification,figures_output_folder)