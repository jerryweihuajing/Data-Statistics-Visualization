# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:22:25 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Consolidation Pressure Calculation
"""

import xlrd
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import operation_list as O_L
import operation_path as O_P
import operation_head_column as O_H_C
import calculation_pressure_consolidation as C_P_C

from o_data import data

#------------------------------------------------------------------------------        
"""
Calculate Pc external interface

Args:
    P: pressure
    e: void ratio
    hole_id: id of hole
    start_depth: start depth of hole
    end_depth: end depth of hole
    output_folder: output folder of figures
    show: whether to show
    
Returns:
    valid list
""" 
def CalculatePc(P,e,hole_id,start_depth,end_depth,output_folder,show=False):
 
    #delete the first element
    valid_P=P[1:]
    valid_e=e[1:]
    
    if valid_P==[] or valid_e==[]:
        
        return None
    
    valid_logP=[np.log10(item) for item in valid_P]
#    valid_logP=[np.log2(item) for item in valid_P]
    
    if C_P_C.CalculatePcAndCc(valid_logP,valid_e)>max(P):
        
        return None
    
    fig,ax=plt.subplots(figsize=(8,8))
    
    final_Pc=C_P_C.CalculatePcAndCc(valid_logP,valid_e,show=show)  
    
    #set ticks
    plt.tick_params(labelsize=12)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    
    #title font
    annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)
    
    #annotation font
    title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)
    
    plt.title('ID:'+str(hole_id),FontProperties=title_font)  
            
    plt.xlabel('lgP',FontProperties=annotation_font)
    plt.ylabel('e',FontProperties=annotation_font)
    
    #label fonts
    for this_label in labels:
        
        this_label.set_fontname('Times New Roman')
        
    #tick step
    x_major_step=(max(valid_logP)-min(valid_logP))/10
    x_minor_step=(max(valid_logP)-min(valid_logP))/20
    y_major_step=(max(valid_e)-min(valid_e))/10
    y_minor_step=(max(valid_e)-min(valid_e))/20
    
    print(P)
    #set locator
    ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
    ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
    
    '''represent A with B'''     
    # plt.xticks(self.list_diameter_lg+[self.list_diameter_lg[-1]+1],self.list_diameter)
        
    ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
    ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
    
    #add depth
    plt.text(np.average(valid_logP),max(valid_e),
             'Start Depth:'+str(start_depth)+'m End Depth:'+str(end_depth)+'m',
             FontProperties=annotation_font)
    
    #show the grid
    plt.grid()
    plt.show()
    
    if final_Pc<100:
        
        output_folder+='0-100\\'
    
    elif final_Pc<200:
        
        output_folder+='100-200\\'
    
    elif final_Pc<400:
        
        output_folder+='200-400\\'
        
    elif final_Pc<800:
        
        output_folder+='400-800\\'
        
    elif final_Pc<1600:
        
        output_folder+='800-1600\\'
        
    else:
        
        output_folder+='1600-3200\\'
        
    fig_path=output_folder+str(hole_id)+'.png'
    
    #save the fig    
    plt.savefig(fig_path,dpi=300,bbox_inches='tight')   
    plt.close()
    
    return final_Pc
 
#------------------------------------------------------------------------------
"""
Make consolidation calculation from one excel

Args:
    xls_path: path of excel to be processed
    num_head_rows: top rows
    num_head_columns: left columns

Returns:
    None
"""
def WorkbookCondolidation(xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Workbook Condolidation')
    
    #plt.style.use('ggplot')
    
    #construct output folder path
    figures_output_folder=xls_path.replace('.xls','').replace('input','output')+'\\'
    
    #generate output folder
    list_threshold=['0-100','100-200','200-400','400-800','800-1600','1600-3200']
    
    for this_threshold in list_threshold:
        
        O_P.GenerateFolder(figures_output_folder+'先期固结压力\\'+this_threshold+'\\')
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
    #data throughout workbook 
    Pc_high_pressure_workbook=[]
    
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
        
        #print(final_head_columns)
        
        #all info of dataframe
        value_matrix=channel.values
        
        #delete the repetition
        index_valid=O_L.ValidIndexList(value_matrix[num_head_rows:,1])  
        
        #fetch the id of P and e
        index_e_high=[]
        
        #pressure
        P_high=[]
        
        index_list=[1,2,3]
        
        #hole id, start depth, end depth
        list_hole_id,\
        list_start_depth,\
        list_end_depth=[O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid) for this_index in index_list]
    
        for k in range(num_head_columns,np.shape(value_matrix)[1]):
            
            #title str
            title=final_head_columns[k] 
                
            if '各级压力下的孔隙比' in title and '高压固结' in title:
                
                print(k,title)
                
                index_e_high.append(k)
                P_high.append(float(title.strip().split(' ')[1]))
                
        #matrix to contain grain partition proportion
        data_e_high=np.zeros((len(index_valid),len(index_e_high)))
                    
        column=0
        
        for this_index in index_e_high:
            
            data_e_high[:,column]=O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid)
        
            column+=1
        
        Pc_high_pressure=[]
        
        #high pressure
        for i in range(np.shape(data_e_high)[0]):
            
            expire_nan_index_list=O_L.ExpireNanIndexList(data_e_high[i])

            this_e=O_L.CustomIndexList(list(data_e_high[i]),expire_nan_index_list)
            this_P=O_L.CustomIndexList(P_high,expire_nan_index_list)
            
            #construct new data object
            that_data=data()
            
            that_data.hole_id=list_hole_id[i]
            that_data.end_depth=list_end_depth[i]
            that_data.start_depth=list_start_depth[i]
            that_data.porosity_compression=this_e
            that_data.pressure_compression=this_P
            
            Pc_high_pressure.append(that_data.ConsolidationCurve(figures_output_folder+'先期固结压力\\'))
            
        Pc_high_pressure_sheet=[]
        
        for j in range(len(index_valid)):
                         
            if Pc_high_pressure[j] is not None:
                
                Pc_high_pressure_sheet.append(Pc_high_pressure[j])
         
        Pc_high_pressure_workbook+=Pc_high_pressure_sheet
            
    fig,ax=plt.subplots(figsize=(8,8))
    
    #for iteration
    list_Pc_worbook=[Pc_high_pressure_workbook]
    list_title=['高压固结']
    
    for k in range(len(list_title)):
        
        #Pc, list title, folder name
        Pc_workbook=list_Pc_worbook[k]
        Pc_title=list_title[k]
        
        if Pc_title=='':
            
            continue
        
        group=np.linspace(min(Pc_workbook),max(Pc_workbook),20)
        
        title_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=16)  
        label_font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=13) 
                
        #plot histogram
        plt.hist(Pc_workbook, group, histtype='bar', rwidth=0.95)
         
        plt.title(Pc_title+'先期固结压力频数分布直方图\n样本总量:'+str(int(len(Pc_workbook))),
                  FontProperties=title_font)  
        
        plt.xlabel('先期固结压力(kPa)',FontProperties=label_font)
            
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
            
        fig_path=figures_output_folder+'先期固结压力\\先期固结压力值分布.png'
        
        plt.savefig(fig_path,dpi=300,bbox_inches='tight')
        plt.close()
    
#path=r'C:\Users\whj\Desktop\fig\\'
#
#P=[0,50,100,200,400,800,1200]
#e=[0.711,0.699,0.692,0.680,0.662,0.640,0.618]
#
#'''position of Pc annotation'''
#pc=CalculatePc(P,e,'GC001-1',1.2,3.4,path,show=True)
