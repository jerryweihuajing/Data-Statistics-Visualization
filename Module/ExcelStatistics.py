# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 21:03:11 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Statistics
"""

import xlrd
import xlwt

import copy as cp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xlutils.copy import copy
from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import HeadColumns as HC
import PathProcessing as PP
import GeotechnicalParameters as GP

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
def SheetsStatistics(xls_path,num_head_rows,num_head_columns,list_num_head_columns=None):
    
    print('')
    print('--Sheets Statistics')
    
    plt.style.use('ggplot')
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #copy former workbook
    new_workbook=copy(workbook)
        
    #construct output folder path
    tables_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\统计\\'
    
    #generate output folder
    PP.GenerateFolder(tables_output_folder)
    
    #save as
    new_workbook.save(tables_output_folder+'统计结果.xls')
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
    #default
    if list_num_head_columns==None:
        
        list_num_head_columns=[num_head_columns]*len(list_sheet_names)
        
    map_sheet_names_num_head_columns=dict(zip(list_sheet_names,list_num_head_columns))    
    
    #traverse all sheets
    for this_sheet_name in workbook.sheet_names():

        print('')
        print('...')
        print('......')
        print('->sheet name:',this_sheet_name)
        print('')
        
        #construct output folder path
        figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\统计\\图\\表 '+this_sheet_name+'\\'
        
        #generate output folder
        PP.GenerateFolder(figures_output_folder)

        #Data Frame object
        channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
        
        final_head_columns,unit_list=HC.HeadColumnsGeneration(channel,num_head_rows)
        
        #print(final_head_columns)
        
        #all info of dataframe
        value_matrix=channel.values
        
        title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
        label_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=13)  
        
        '''complete info of statistics'''
            
        #item names of statistics
        statistic_items=['数据量','最大值','最小值','平均值','标准差','变异系数','标准值']
        
        #new dataframe to store statistic data
        statistic=cp.deepcopy(channel.iloc[:len(statistic_items)])
        
        #columns to delete
        columns_to_delete=[]
        
        #no valid data
        columns_void=[]
        
        for k in range(num_head_columns,np.shape(value_matrix)[1]):
        
            #num of steps
            n_step=20
            
            #fetch the data
            data=list(value_matrix[num_head_rows:,k])
            
            #unit str
            unit=unit_list[k]
            
            #title str
            title=final_head_columns[k]
            
            #expire particular conditions
            if '分类' in title or '备' in title or '注' in title:
                
                #give the value
                statistic.iloc[0,k]=''
                statistic.iloc[1,k]=''
                statistic.iloc[2,k]=''
                statistic.iloc[3,k]=''
                statistic.iloc[4,k]=''
                statistic.iloc[5,k]=''
                statistic.iloc[6,k]=''
                
                columns_to_delete.append(title)
                
                #expire nan
                valid_str=[this_data for this_data in data if isinstance(this_data,str)]
                
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
                
                ax.yaxis.set_major_locator(MultipleLocator(int(np.ceil((max(str_frequency)-min(str_frequency))/n_step))))
                
                #set ticks
                plt.tick_params(labelsize=60/len(str_group))
        
                #y label fonts
                for this_label in ax.get_yticklabels():
                    
                    this_label.set_fontname('Times New Roman')
                    
                #x label fonts
                for this_label in ax.get_xticklabels():
                    
                    this_label.set_fontname('SimHei')
                    
                plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_str))),
                          FontProperties=title_font)
                
                plt.xlabel(title+' '+unit,FontProperties=label_font)
                
                plt.savefig(figures_output_folder+title+'.png')
                plt.close()
                
                continue
            
            #expire nan
            valid_data=[float(this_data) for this_data in data if not np.isnan(float(this_data))]
            
            print(k,title)
        
            if valid_data==[]:
                
                #give the value
                statistic.iloc[0,k]=''
                statistic.iloc[1,k]=''
                statistic.iloc[2,k]=''
                statistic.iloc[3,k]=''
                statistic.iloc[4,k]=''
                statistic.iloc[5,k]=''
                statistic.iloc[6,k]=''
                
                columns_void.append(title)
                
                continue
            
            #x coordinates
            group=np.linspace(min(valid_data),max(valid_data),n_step)
        
            #whether to process
            scaled_flag=False
            
            #exception processing
            for this_tick in group:
                
                if 'e' in str(this_tick):
                    
        #            print(str(min(group)).split('e')[0])
        #            print(str(max(group)).split('e')[0])
        #            print(str(min(group)).split('e')[-1])
        #            print(str(max(group)).split('e')[-1])
        
                    factor=str(min(group)).split('e')[-1]
        
                    scaled_flag=True
                    
                    break
                
            fig,ax=plt.subplots(figsize=(8,8))
            
            if scaled_flag:
                    
                #mutiply a factor
                valid_data=np.array(valid_data)/10**(int(factor))
                        
                group=np.linspace(min(valid_data),max(valid_data),n_step)  
                
                #plot histogram
                plt.hist(valid_data, group, histtype='bar', rwidth=0.95)
                 
                plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_data))),
                          FontProperties=title_font)
                
                plt.xlabel(title+' e'+factor+' '+unit,FontProperties=label_font)
            
            else:
                
                #plot histogram
                plt.hist(valid_data, group, histtype='bar', rwidth=0.95)
                 
                plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_data))),
                          FontProperties=title_font)  
                
                plt.xlabel(title+' '+unit,FontProperties=label_font)
            
            #list of frequency
            frequency=[0]*(len(group)-1)
            
            #mannual histogram
            for this_valid_data in valid_data:
        
                for g in range(len(group)-1):
                    
                    if group[g]<=this_valid_data<=group[g+1]:
                        
                        frequency[g]+=1
                        
                        break
         
            ax.yaxis.set_major_locator(MultipleLocator(int(np.ceil((max(frequency)-min(frequency))/n_step))))
            
            #set ticks
            plt.tick_params(labelsize=15)
            labels = ax.get_xticklabels() + ax.get_yticklabels()
            
            #label fonts
            for this_label in labels:
                
                this_label.set_fontname('Times New Roman')
                
            #amount
            data_amount=len(valid_data)
            
            #maximum
            data_maximum=np.max(valid_data)
            
            #minimum
            data_minimum=np.min(valid_data)  
            
            #average
            data_average=np.mean(valid_data)
            
            #standard deviation
            data_standard_deviation=GP.StandardDeviation(valid_data)
            
            #variable coefficient
            data_variable_coefficient=GP.VariableCoefficient(valid_data)
            
            #standard value
            data_standard_value=GP.StandardValue(valid_data,'+')
            
            #give the value
            statistic.iloc[0,k]=data_amount
            statistic.iloc[1,k]=data_maximum
            statistic.iloc[2,k]=data_minimum
            statistic.iloc[3,k]=data_average
            statistic.iloc[4,k]=data_standard_deviation
            statistic.iloc[5,k]=data_variable_coefficient
            statistic.iloc[6,k]=data_standard_value
            
            #valid file name
            if '<' in title:
                
                title=title.replace('<','小于')
                
            if '>' in title:
                
                title=title.replace('>','大于')    
            
            plt.savefig(figures_output_folder+title+'.png')
            plt.close()
            
        #statistics decoration
        for k in range(len(statistic_items)):
            
            statistic.iloc[k,1]=statistic_items[k]
          
        #delete one column
        statistic=statistic.drop(statistic.columns[0],axis=1,index=None)
        
        #rename column
        statistic=statistic.rename(columns = {statistic.columns[1]:'特征值'})  
        
        #index of line where info starts
        start_info_row=num_head_rows+1
          
        #open a sheet
        this_sheet=new_workbook.get_sheet(this_sheet_name)   
         
        #total lines
        num_info_rows=len(this_sheet.rows)
        
        #blank row
        one_list=['']*(len(channel.iloc[:1].columns)+2)
        
        #define the border style
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour=0x3A    
         
        style = xlwt.XFStyle()
        style.borders = borders
        
        #fill with blank lines
        for ii in range(num_info_rows):
            
            for jj in range(len(one_list)):
                
                this_sheet.write(ii+start_info_row,jj,one_list[jj])
        
        '''Data frame reads data and automatically ignores empty rows and columns'''
        for i in range(statistic.shape[0]):
            
            for j in range(statistic.shape[1]):
              
                try:
                    
                    this_sheet.write(i+start_info_row,
                                     j+map_sheet_names_num_head_columns[this_sheet_name],
                                     statistic.iloc[i,j],
                                     style)      
                  
                #transform int to float
                except:
                    
                    this_sheet.write(i+start_info_row,
                                     j+map_sheet_names_num_head_columns[this_sheet_name],
                                     float(statistic.iloc[i,j]),
                                     style)
   
        new_workbook.save(tables_output_folder+'统计结果.xls')
             
#------------------------------------------------------------------------------
"""
Make statistics from one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns

Returns:
    None
"""
def WorkbookStatistics(xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Workbook Statistics')
    
    plt.style.use('ggplot')
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #construct output folder path
    tables_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\统计\\'
    
    #construct output folder path
    figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\统计\\图\\总表\\'
        
    #generate output folder
    PP.GenerateFolder(tables_output_folder)
    PP.GenerateFolder(figures_output_folder)
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
     
    '''title and data throughout whole workbook'''
    list_title=[]
    list_data=[]
    
    #traverse all sheets
    for this_sheet_name in list_sheet_names:
    
        print('')
        print('...')
        print('......')
        print('->sheet name:',this_sheet_name)
        print('')
        
        #generate output folder
        PP.GenerateFolder(figures_output_folder)
    
        #Data Frame object
        channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
        
        final_head_columns,unit_list=HC.HeadColumnsGeneration(channel,num_head_rows)
        
        #print(final_head_columns)
        
        #all info of dataframe
        value_matrix=channel.values
        
        title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
        label_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=13)  
        
        '''complete info of statistics'''
            
        #item names of statistics
        statistic_items=['数据量','最大值','最小值','平均值','标准差','变异系数','标准值']
        
        #columns to delete
        columns_to_delete=[]
        
        #no valid data
        columns_void=[]
        
        for k in range(num_head_columns,np.shape(value_matrix)[1]):
        
            #num of steps
            n_step=20
            
            #fetch the data
            data=list(value_matrix[num_head_rows:,k])
            
            #unit str
            unit=unit_list[k]
            
            #title str
            title=final_head_columns[k]
            
            list_data.append(data)
            list_title.append(title)
   
    #map between title and data
    map_title_data={}
    
    for k in range(len(list_title)):
        
        this_title=list_title[k]
        this_data=list_data[k]
        
        if this_title in list(map_title_data.keys()):
            
            map_title_data[this_title]+=this_data
            
        else:
            
            map_title_data[this_title]=this_data
     
    #new matrix to contain statistic result
    statistic=[len(map_title_data)*['']]*len(statistic_items)
    
    #traverse the dictionary
    for k in range(len(map_title_data)):
        
        title=list(map_title_data.keys())[k]
        data=list(map_title_data.values())[k]
        
        #expire particular conditions
        if '分类' in title or '备' in title or '注' in title:
            
            #give the value
            for this_line in statistic:
                
                this_line[k]=''
    
            columns_to_delete.append(title)
            
            #expire nan
            valid_str=[this_data for this_data in data if isinstance(this_data,str)]
            
            #group in x axis
            str_group=list(set(valid_str))
            
            #list of str frequency
            str_frequency=[0]*(len(str_group))
                  
            #construct a dictionary as vote machine
            map_str_frequency=dict((this_valid_str,valid_str.count(this_valid_str)) for this_valid_str in valid_str)
            
    #        print(map_str_frequency)
           
            #frequency list
            str_frequency=list(map_str_frequency.values())
            
            fig,ax=plt.subplots(figsize=(12,8))
            
            '''transform orientation'''
            #plot histogram
            plt.barh(range(len(str_frequency)),str_frequency,tick_label=str_group)
            
            ax.xaxis.set_major_locator(MultipleLocator(int(np.ceil((max(str_frequency)-min(str_frequency))/n_step))))
            
            #set ticks
            plt.tick_params(labelsize=12)
    
            #y label fonts
            for this_label in ax.get_xticklabels():
                
                this_label.set_fontname('Times New Roman')
                
            #x label fonts
            for this_label in ax.get_yticklabels():
                
                this_label.set_fontname('SimHei')
                
            plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_str))),
                      FontProperties=title_font)
            
            plt.savefig(figures_output_folder+title+'.png')
            plt.close()
            
            continue
        
        #expire nan
        valid_data=[float(this_data) for this_data in data if not np.isnan(float(this_data))]
        
        print(k,title)
    
        if valid_data==[]:
            
            #give the value
            for this_line in statistic:
                
                this_line[k]=''
            
            columns_void.append(title)
            
            continue
        
        #x coordinates
        group=np.linspace(min(valid_data),max(valid_data),n_step)
    
        #whether to process
        scaled_flag=False
        
        #exception processing
        for this_tick in group:
            
            if 'e' in str(this_tick):
                
    #            print(str(min(group)).split('e')[0])
    #            print(str(max(group)).split('e')[0])
    #            print(str(min(group)).split('e')[-1])
    #            print(str(max(group)).split('e')[-1])
    
                factor=str(min(group)).split('e')[-1]
    
                scaled_flag=True
                
                break
            
        fig,ax=plt.subplots(figsize=(8,8))
        
        if scaled_flag:
                
            #mutiply a factor
            valid_data=np.array(valid_data)/10**(int(factor))
                    
            group=np.linspace(min(valid_data),max(valid_data),n_step)  
            
            #plot histogram
            plt.hist(valid_data, group, histtype='bar', rwidth=0.95)
             
            plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_data))),
                      FontProperties=title_font)
            
            plt.xlabel(title+' e'+factor+' '+unit,FontProperties=label_font)
        
        else:
            
            #plot histogram
            plt.hist(valid_data, group, histtype='bar', rwidth=0.95)
             
            plt.title(title+' 频数分布直方图\n样本总量:'+str(int(len(valid_data))),
                      FontProperties=title_font)  
            
            plt.xlabel(title+' '+unit,FontProperties=label_font)
        
        #list of frequency
        frequency=[0]*(len(group)-1)
        
        #mannual histogram
        for this_valid_data in valid_data:
    
            for g in range(len(group)-1):
                
                if group[g]<=this_valid_data<=group[g+1]:
                    
                    frequency[g]+=1
                    
                    break
     
        ax.yaxis.set_major_locator(MultipleLocator(int(np.ceil((max(frequency)-min(frequency))/n_step))))
        
        #set ticks
        plt.tick_params(labelsize=15)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        
        #label fonts
        for this_label in labels:
            
            this_label.set_fontname('Times New Roman')
            
        #amount
        data_amount=len(valid_data)
        
        #maximum
        data_maximum=np.max(valid_data)
        
        #minimum
        data_minimum=np.min(valid_data)  
        
        #average
        data_average=np.mean(valid_data)
        
        #standard deviation
        data_standard_deviation=GP.StandardDeviation(valid_data)
        
        #variable coefficient
        data_variable_coefficient=GP.VariableCoefficient(valid_data)
        
        #standard value
        data_standard_value=GP.StandardValue(valid_data,'+')
        
        #give the value
        statistic[0][k]=str(round(data_amount,3))
        statistic[1][k]=str(round(data_maximum,3))
        statistic[2][k]=str(round(data_minimum,3))
        statistic[3][k]=str(round(data_average,3))
        statistic[4][k]=str(round(data_standard_deviation,3))
        statistic[5][k]=str(round(data_variable_coefficient,3))
        statistic[6][k]=str(round(data_standard_value,3))
        
        #valid file name
        if '<' in title:
            
            title=title.replace('<','小于')
            
        if '>' in title:
            
            title=title.replace('>','大于')    
        
        plt.savefig(figures_output_folder+title+'.png')
        plt.close()
            
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
    
    #decoration
    plus=1
    
    #title
    new_sheet.write(0,0,'特征值',style)
    
    #header
    for kk in range(len(map_title_data)):
        
        this_title=list(map_title_data.keys())[kk]
        
        new_sheet.write(kk+1,0,this_title,style)
        
    #items
    for kk in range(len(statistic_items)):
        
        this_item=statistic_items[kk]
        
        new_sheet.write(0,kk+plus,this_item,style)
        
    for i in range(len(statistic_items)):
        
        for j in range(len(map_title_data)):
          
            try:
                
                new_sheet.write(j+1,i+plus,statistic[i][j],style)      
              
            #transform int to float
            except:
                
                new_sheet.write(j+plus,i+plus,float(statistic[i,j]),style)
       
    new_workbook.save(tables_output_folder+'统计总表.xls')
