# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 21:49:46 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Data Filering and Stastics
"""

import xlrd
import xlwt

import pandas as pd
from xlutils.copy import copy

import HeadColumns as HC
import ListOperation as LO
import PathProcessing as PP

#------------------------------------------------------------------------------
"""
Make data filtering from all sheets in one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    
Returns:
    None
"""
def SheetsFiltering(xls_path,num_head_rows):
    
    #concat different sheets in a workbook
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #copy former workbook
    new_workbook=copy(workbook)
        
    #construct output folder path
    tables_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\统计\\'
    
    #generate output folder
    PP.GenerateFolder(tables_output_folder)
    
    #save as
    new_workbook.save(tables_output_folder+'筛选结果.xls')
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
        
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
        
        #delete the repetition
        index_valid=LO.ValidIndexList(value_matrix[num_head_rows:,1])
        
        #delete lines
        index_to_delete=LO.SetDiffernece(range(len(value_matrix[:,1])-num_head_rows),index_valid)
        
        #define the index
        channel.index=pd.Series(range(len(channel)))
        
        #delete a batch of lines based on index
        final_channel=channel.drop([this_index+num_head_rows for this_index in index_to_delete])
        
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
        
        #delete invalid lines
        final_channel=final_channel.drop(range(num_head_rows))
        
        '''Data frame reads data and automatically ignores empty rows and columns'''
        for i in range(final_channel.shape[0]):
            
            for j in range(final_channel.shape[1]):
              
                try:
                    
                    this_sheet.write(i+start_info_row,
                                     j,
                                     final_channel.iloc[i,j],
                                     style)      
                  
                #transform int to float
                except:
                    
                    this_sheet.write(i+start_info_row,
                                     j,
                                     float(final_channel.iloc[i,j]),
                                     style)
       
        new_workbook.save(tables_output_folder+'筛选结果.xls')