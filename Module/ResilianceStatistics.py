# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 20:47:26 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Consolidation Calculation
"""

import xlrd
import pandas as pd

import HeadColumns as HC
import ListOperation as LO
import PathProcessing as PP

from o_data import data

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

def ResilianceVisualization(valid_logP_resiliance,valid_e_resiliance):
    
    #combine x y
    which_x_y=[[valid_logP_resiliance[k],valid_e_resiliance[k]] for k in range(len(x))]
    
    #result of interpolation
    new_x_y=LargrangeInterpolation(x,y)
    
    new_x=[this_x_y[0] for this_x_y in new_x_y]
    new_y=[this_x_y[1] for this_x_y in new_x_y]
    
#------------------------------------------------------------------------------
"""
Make resiliance calculation from one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns

Returns:
    None
"""
def WorkbookResiliance(xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Resiliance Calculation')
    
    #plt.style.use('ggplot')
    
    #construct output folder path
    figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\'
    
    #generate output folder   
    PP.GenerateFolder(figures_output_folder+'Pc\\回弹\\')  

    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
    #data throughout workbook 
    Pc_compress_workbook=[]
    Pc_resiliance_workbook=[]
    Pc_recompress_workbook=[]
    
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
        
#        print(final_head_columns)
        
        #all info of dataframe
        value_matrix=channel.values
        
        #delete the repetition
        index_valid=LO.ValidIndexList(value_matrix[num_head_rows:,1])  

        #fetch the id of P and e
        index_settlement_compression=[]
        index_settlement_resiliance=[]
        index_settlement_recompression=[]
        
        #pressure
        pressure_compression=[]
        pressure_resiliance=[]
        pressure_recompression=[]
    
        for k in range(num_head_columns,np.shape(value_matrix)[1]):
            
            #title str
            title=final_head_columns[k] 
               
            if '孔隙比' in title:
                
                print(k,title)
                
                index_porosity_original=k
                
            if '压缩指数' in title:
                
                print(k,title)
                
                index_coefficient_compression=k
                
            if '回弹指数' in title:
                
                print(k,title)
                
                index_coefficient_resiliance=k
                
            if '一定压力固结沉降量' in title:
                
                print(k,title)
                
                index_settlement_compression.append(k)

                pressure_compression.append(float(title.strip().split(' ')[1].replace('kPa','')))
                
            if '回弹固结沉降量' in title:
                
                print(k,title)
                
                index_settlement_resiliance.append(k)
                pressure_resiliance.append(float(title.strip().split(' ')[1]))
                
            if '再压缩固结沉降量' in title:
                
                if 'PC' in title or '指数' in title:
                    
                    continue
                
                print(k,title)
                
                index_settlement_recompression.append(k)
                pressure_recompression.append(float(title.strip().split(' ')[1]))
            
        #hole id
        list_hole_id=LO.CustomIndexList(list(value_matrix[num_head_rows:,1]),index_valid)
        
        #start depth
        list_start_depth=LO.CustomIndexList(list(value_matrix[num_head_rows:,2]),index_valid)
        
        #end depth
        list_end_depth=LO.CustomIndexList(list(value_matrix[num_head_rows:,3]),index_valid)
        
        #pore aperture
        list_porosity_original=LO.CustomIndexList(list(value_matrix[num_head_rows:,index_porosity_original]),index_valid)
        
        #compression coefficient
        list_coefficient_compression=LO.CustomIndexList(list(value_matrix[num_head_rows:,index_coefficient_compression]),index_valid)
        
        #resiliance coefficient
        list_coefficient_resiliance=LO.CustomIndexList(list(value_matrix[num_head_rows:,index_coefficient_resiliance]),index_valid)
        
        list_index=[index_settlement_compression,
                    index_settlement_resiliance,
                    index_settlement_recompression]
        
        list_data=[]
        
        for this_index_list in list_index:
            
            #matrix to contain grain partition proportion    
            this_data=np.zeros((len(index_valid),len(this_index_list)))
            
            column=0
                
            for this_index in this_index_list:
                
                this_data[:,column]=LO.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid)
            
                column+=1
                
            list_data.append(this_data)
        
        data_settlement_compression,\
        data_settlement_resiliance,\
        data_settlement_recompression=list_data
        
        #construct data object
        for i in range(len(index_valid)):
            
            that_data=data()
            
            that_data.hole_id=list_hole_id[i]
            that_data.end_depth=list_end_depth[i]
            that_data.start_depth=list_start_depth[i]
            that_data.porosity_original=list_porosity_original[i]
            that_data.coefficient_compression=list_coefficient_compression[i]
            that_data.coefficient_resiliance=list_coefficient_resiliance[i]
            
            that_data.pressure_compression=pressure_compression
            that_data.pressure_resiliance=pressure_resiliance
            that_data.pressure_recompression=pressure_recompression
            
            that_data.settlement_compression=data_settlement_compression[i]
            that_data.settlement_resiliance=data_settlement_resiliance[i]
            that_data.settlement_recompression=data_settlement_recompression[i]
            
#            print(that_data.settlement_pressure)
#            print(that_data.settlement_resiliance)
#            print(that_data.settlement_recompress)
            
            print(that_data.porosity_original)
#            print(that_data.coefficient_compression)
#            print(that_data.coefficient_resiliance)
            
            print(that_data.pressure_compression)
#            print(that_data.pressure_resiliance)
#            print(that_data.pressure_recompression)
            
            '''unit of coeffient is 1/MPa'''
            #define the porosity:alpha=de/dp
            that_data.porosity_compression=that_data.porosity_original\
                                          -0.001*that_data.coefficient_compression\
                                          *np.array(that_data.pressure_compression)
                                            
            that_data.porosity_resiliance=that_data.porosity_original\
                                         -0.001*that_data.coefficient_resiliance\
                                         *np.array(that_data.pressure_resiliance)
                                            
            that_data.porosity_recompression=that_data.porosity_original\
                                            -0.001*that_data.coefficient_compression\
                                            *np.array(that_data.pressure_recompression)
            
            print(that_data.porosity_compression)
#            print(that_data.porosity_resiliance)
#            print(that_data.porosity_recompression)
                                            
#            that_data.Canvas(figures_output_folder+'Pc\\回弹\\')
            
#        #high pressure
#        for i in range(np.shape(index_valid)[0]):
#            
#            expire_nan_index_list=LO.ExpireNanIndexList(data_e_high[i])
#        
#            this_e=LO.CustomIndexList(list(data_e_high[i]),expire_nan_index_list)
#            this_P=LO.CustomIndexList(P_high,expire_nan_index_list)
#            
#            this_hole_id=list_hole_id[i]
#            this_start_depth=list_start_depth[i]
#            this_end_depth=list_end_depth[i]
#            
#            Pc_high_pressure.append(CalculatePc(this_P,
#                                                this_e,
#                                                this_hole_id,
#                                                this_start_depth,
#                                                this_end_depth,
#                                                figures_output_folder+'Pc\\高压\\',
#                                                show=True))
#            
#        Pc_normal_sheet=[]
#        Pc_high_pressure_sheet=[]
#        
#        for j in range(len(index_valid)):
#            
#    #        print(Pc_normal[j],Pc_high_pressure[j])
#            
#            if Pc_normal[j] is None and Pc_high_pressure[j] is None:
#                
#                continue
#            
#            if Pc_normal[j] is not None:
#                
#                 Pc_normal_sheet.append(Pc_normal[j])
#                
#            if Pc_high_pressure[j] is not None:
#                
#                Pc_high_pressure_sheet.append(Pc_high_pressure[j])
#         
#        Pc_normal_workbook+=Pc_normal_sheet
#        Pc_high_pressure_workbook+=Pc_high_pressure_sheet
#            
#    fig,ax=plt.subplots(figsize=(8,8))
#    
#    #for iteration
#    list_Pc_worbook=[Pc_normal_workbook,Pc_high_pressure_workbook]
#    list_title=['','高压固结']
#    list_folder_name=['正常\\','高压\\']
#    
#    for k in range(len(list_title)):
#        
#        #Pc, list title, folder name
#        Pc_workbook=list_Pc_worbook[k]
#        Pc_title=list_title[k]
#        Pc_folder_name=list_folder_name[k]
#        
#        if Pc_title=='':
#            
#            continue
#        
#        group=np.linspace(min(Pc_workbook),max(Pc_workbook),20)
#        
#        title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
#        label_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=13) 
#                
#        #plot histogram
#        plt.hist(Pc_workbook, group, histtype='bar', rwidth=0.95)
#         
#        plt.title(Pc_title+'Pc频数分布直方图\n样本总量:'+str(int(len(Pc_workbook))),
#                  FontProperties=title_font)  
#        
#        plt.xlabel('Pc(kPa)',FontProperties=label_font)
#            
#        #list of frequency
#        frequency=[0]*(len(group)-1)
#        
#        #mannual histogram
#        for this_valid_data in Pc_workbook:
#        
#            for g in range(len(group)-1):
#                
#                if group[g]<=this_valid_data<=group[g+1]:
#                    
#                    frequency[g]+=1
#                    
#                    break
#         
#        ax.yaxis.set_major_locator(MultipleLocator(int(np.ceil((max(frequency)-min(frequency))/20))))
#        
#        #set ticks
#        plt.tick_params(labelsize=15)
#        labels = ax.get_xticklabels() + ax.get_yticklabels()
#        
#        #label fonts
#        for this_label in labels:
#            
#            this_label.set_fontname('Times New Roman')
#            
#        plt.savefig(figures_output_folder+'Pc\\'+Pc_folder_name+'Pc值分布.png')
#        plt.close()
        