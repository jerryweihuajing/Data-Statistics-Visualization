# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:41:14 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Stastics of Diameter Curve
"""

import xlrd,xlwt
import numpy as np
import pandas as pd

import operation_head_column as O_H_C
import operation_list as O_L
import operation_path as O_P

#------------------------------------------------------------------------------
"""
Make resilience curve from one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns

Returns:
    None
"""
def WorkbookDiameter(xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Workbook Diameter')
    
    #plt.style.use('ggplot')
    
    #construct output folder path
    output_folder=xls_path.replace('.xls','').replace('input','output')+'\\先期固结压力\\回弹\\'
    
    #generate output folder
    O_P.GenerateFolder(output_folder)
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
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
    
    #traverse all sheets
    for this_sheet_name in list_sheet_names:
    
        print('')
        print('...')
        print('......')
        print('->sheet name:',this_sheet_name)
        print('')
        
        #Data Frame object
        channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
        
        final_head_columns,unit_list=O_H_C.HeadColumnsGeneration(channel,num_head_rows)
        
#        print(final_head_columns)
        
        #all info of dataframe
        value_matrix=channel.values
        
        '''special condition'''
        num_head_rows-=1
        
        #delete the repetition
        index_valid=O_L.ValidIndexList(value_matrix[num_head_rows:,1])  

        #fetch the id of P and e
        index_settlement_compression=[]
        index_settlement_resilience=[]
        index_settlement_recompression=[]
        
        #pressure
        pressure_compression=[]
        pressure_resilience=[]
        pressure_recompression=[]
    
        for k in range(num_head_columns,np.shape(value_matrix)[1]):
            
            #title str
            title=final_head_columns[k] 
               
            if 'PC' in title:
                
                print(k,title)
                
                index_pressure_consolidation=k
                
            if '压缩指数' in title:
                
                print(k,title)
                
                index_index_compression=k
                
            if '回弹指数' in title:
                
                print(k,title)
                
                index_index_resilience=k    
                
            if '孔隙比' in title:
                
                print(k,title)
                
                index_porosity_original=k
                
            if '一定压力固结沉降量' in title:
                
                print(k,title)
                
                index_settlement_compression.append(k)

                pressure_compression.append(float(title.strip().split(' ')[1].replace('kPa','')))
                
            if '回弹固结沉降量' in title:
                
                print(k,title)
                
                index_settlement_resilience.append(k)
                pressure_resilience.append(float(title.strip().split(' ')[1]))
                
            if '再压缩固结沉降量' in title:
                
                if 'PC' in title or '指数' in title:
                    
                    continue
                
                print(k,title)
                
                index_settlement_recompression.append(k)
                pressure_recompression.append(float(title.strip().split(' ')[1]))