# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:41:14 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Stastics of Diameter Curve
"""

import xlrd
import copy as cp
import numpy as np
import pandas as pd

import operation_head_column as O_H_C
import operation_list as O_L
import operation_path as O_P

from o_data import data

diameter_range=[200,20,2,0.5,0.25,0.075,0.05,0.005,0]

#------------------------------------------------------------------------------
"""
Combine data object with the same id

Args:
    list_layer: layer data object list

Returns:
    combined data object list
"""
def MapIdData2Data(map_id_data):
    
    list_data=[]
    
    for item in list(map_id_data.items()):
            
        new_data=data()
        
        new_data.hole_id=item[0]
        
        #data in this hole
        list_layer_this_hole=item[1]
        
        list_list_diameter_percentage=[]
        
        #thickness of layer
        list_thickness=[]
        
        for this_data in list_layer_this_hole:
              
            list_list_diameter_percentage.append(this_data.list_diameter_percentage)
           
            list_thickness.append(this_data.end_depth-this_data.start_depth)
              
        new_data.list_diameter=cp.deepcopy(diameter_range)
        
        #accumulate the diameter percentage
        new_data.list_diameter_percentage=np.array([0.0]*len(new_data.list_diameter))
        
        for this_list in list_list_diameter_percentage:
            
            for k in range(len(this_list)):
                
                if np.isnan(this_list[k]):
                    
                    this_list[k]=0
                    
        #weight of average
        list_weight=np.array(list_thickness)/np.sum(list_thickness)
        
        for i in range(len(list_weight)):

            new_data.list_diameter_percentage+=list_weight[i]*np.array(list_list_diameter_percentage[i])
        
        new_data.list_diameter_percentage=list(new_data.list_diameter_percentage)
        
        for kk in range(len(new_data.list_diameter_percentage)):
            
            if new_data.list_diameter_percentage[kk]==0:
                
                new_data.list_diameter_percentage[kk]=np.nan

        list_bool=[np.isnan(this_percentage) for this_percentage in new_data.list_diameter_percentage]
   
        #expire list with all nan
        if list_bool==len(list_bool)*[True]:
            
            continue
        
        #calculate the cumulative percentage
        new_data.list_diameter_percentage_cumulative=[]
        
        for s in range(len(new_data.list_diameter_percentage)):
            
            this_cumulative_percentage=np.sum([this_percentage for this_percentage in new_data.list_diameter_percentage[s:] if not np.isnan(this_percentage)])
            
            new_data.list_diameter_percentage_cumulative.append(this_cumulative_percentage)
            
        #collect this data list
        new_data.list_data=list_layer_this_hole
        
        list_data.append(new_data)
        
    return list_data
        
#------------------------------------------------------------------------------
"""
Transform layer list to hole list

Args:
    list_layer: layer data object list

Returns:
    hole data object list
"""
def Layer2Hole(list_layer):
    
    #construct hole objects
    list_hole=[]
    
    map_id_hole={}
    
    #combine layer data to hole data
    for this_layer in list_layer:
        
        this_hole_id=this_layer.hole_id.split('-')[0]
        
        if this_hole_id not in list(map_id_hole.keys()):
            
            map_id_hole[this_hole_id]=[]

        map_id_hole[this_hole_id].append(this_layer)
        
    #construct hole objects
    list_hole=MapIdData2Data(map_id_hole)
    
    #define the depth
    for this_hole in list_hole:
        
        list_depth_this_hole=[this_data.start_depth for this_data in this_hole.list_data]
        list_depth_this_hole+=[this_data.end_depth for this_data in this_hole.list_data]
    
        this_hole.end_depth=np.max(list_depth_this_hole)
        this_hole.start_depth=np.min(list_depth_this_hole)
        
    return list_hole
            
#------------------------------------------------------------------------------
"""
Transform data list to range data list

Args:
    list_layer: layer data object list

Returns:
    range data object list
"""
def Data2RangeData(list_data):
    
    map_id_range_data={}
    
    #combine data data to hole data
    for this_data in list_data:
        
        left_depth=3*int(this_data.end_depth//3)
        right_depth=left_depth+3

        #id of range data
        range_data_id=str(int(left_depth))+'-'+str(int(right_depth))+'(m)'
        
        if range_data_id not in list(map_id_range_data.keys()):
            
            map_id_range_data[range_data_id]=[]
            
        if left_depth<=this_data.end_depth<=right_depth:
            
            map_id_range_data[range_data_id].append(this_data)
            
    #construct range data objects
    list_range_data=MapIdData2Data(map_id_range_data)     
    
    #define the depth
    for this_range_data in list_range_data:
        
        this_range_data.start_depth=int(this_range_data.hole_id.strip('(m)').split('-')[0])
        this_range_data.end_depth=int(this_range_data.hole_id.strip('(m)').split('-')[1])
        
    return list_range_data

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
    print('-- Workbook Diameter')
    
    #plt.style.use('ggplot')
    
    #construct output folder path
    output_folder=xls_path.replace('.xls','').replace('input','output')+'\\粒径曲线\\'
    
    #generate output folder
    O_P.GenerateFolder(output_folder)
    
    #open the excel sheet to be operated on
    #formatting_info: keep the header format
    workbook=xlrd.open_workbook(xls_path,formatting_info=True)
    
    #construct map between sheet names and head rows
    list_sheet_names=list(workbook.sheet_names())
    
    #traverse all sheets
    for this_sheet_name in list_sheet_names[:-1]:
        
        O_P.GenerateFolder(output_folder+this_sheet_name+'\层划分集合\\')
        O_P.GenerateFolder(output_folder+this_sheet_name+'\孔划分集合\\')
        O_P.GenerateFolder(output_folder+this_sheet_name+'\层划分\\')
        O_P.GenerateFolder(output_folder+this_sheet_name+'\孔划分\\')
        O_P.GenerateFolder(output_folder+this_sheet_name+'\孔集合\\')
        O_P.GenerateFolder(output_folder+this_sheet_name+'\孔\\')
        O_P.GenerateFolder(output_folder+this_sheet_name+'\层\\')
        
        print('')
        print('...')
        print('......')
        print('-> sheet name:',this_sheet_name)
        print('')
        
        #Data Frame object
        channel=pd.read_excel(xls_path,sheet_name=this_sheet_name)
        
        final_head_columns,unit_list=O_H_C.HeadColumnsGeneration(channel,num_head_rows)
        
#        print(final_head_columns)
        
        #all info of dataframe
        value_matrix=channel.values
        
#        '''special condition'''
#        num_head_rows-=1
        
        #delete the repetition
        index_valid=O_L.ValidIndexList(value_matrix[num_head_rows:,1])  
    
        index_diameter=[]

        for k in range(num_head_columns,np.shape(value_matrix)[1]):
            
            #title str
            title=final_head_columns[k] 
               
            if '颗' in title\
            and '粒' in title\
            and '分' in title\
            and '析' in title\
            and 'mm' in title:
                
                print(k,title)
                
                index_diameter.append(k)
 
        index_list=[0,1,2,3]
        
        #indoor id, hole id, start depth, end depth, 
        #pore aperture, consolidation pressure, compression index, resilience index
        list_indoor_id,\
        list_hole_id,\
        list_start_depth,\
        list_end_depth=[O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid) for this_index in index_list]
        
        #matrix to contain grain partition proportion
        layers_diameter=np.zeros((len(index_valid),len(index_diameter)))
        
        column=0
        
        for this_index in index_diameter:
            
            layers_diameter[:,column]=O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid)
        
            column+=1
              
        #construct data objects
        list_layer=[]
        
        for i in range(np.shape(layers_diameter)[0]):
            
            new_layer=data()
            
            new_layer.hole_id=list_hole_id[i]
            new_layer.indoor_id=list_indoor_id[i]
            new_layer.end_depth=list_end_depth[i]
            new_layer.start_depth=list_start_depth[i]
            
            new_layer.list_diameter=cp.deepcopy(diameter_range)
            new_layer.list_diameter_percentage=list(layers_diameter[i,:])

            list_bool=[np.isnan(this_percentage) for this_percentage in new_layer.list_diameter_percentage]
            
            #expire list with all nan
            if list_bool==len(list_bool)*[True]:
                
                continue
            
            #calculate the cumulative percentage
            new_layer.list_diameter_percentage_cumulative=[]
            
            for s in range(len(new_layer.list_diameter_percentage)):
                
                this_cumulative_percentage=np.sum([this_percentage for this_percentage in new_layer.list_diameter_percentage[s:] if not np.isnan(this_percentage)])
                
                new_layer.list_diameter_percentage_cumulative.append(this_cumulative_percentage)
                
            list_layer.append(new_layer)
                   
            #Generate hole list
            list_hole=Layer2Hole(list_layer)
            
            #Generate range layer list
            list_range_layer=Data2RangeData(list_layer)
            
            #Generate range hole list
            list_range_hole=Data2RangeData(list_hole)
            
        #output the visualization
        for this_layer in list_layer:
            
            this_layer.DiameterCurve(output_folder+this_sheet_name+'\层\\')
            
        for this_hole in list_hole:
            
            this_hole.DiameterCurve(output_folder+this_sheet_name+'\孔\\')
            this_hole.DiameterCurveBatch(output_folder+this_sheet_name+'\孔集合\\')  
            
        for this_range_layer in list_range_layer:
            
            this_range_layer.DiameterCurve(output_folder+this_sheet_name+'\层划分\\')
            this_range_layer.DiameterCurveBatch(output_folder+this_sheet_name+'\层划分集合\\')  
            
        for this_range_hole in list_range_hole:
            
            this_range_hole.DiameterCurve(output_folder+this_sheet_name+'\孔划分\\')
            this_range_hole.DiameterCurveBatch(output_folder+this_sheet_name+'\孔划分集合\\')  
            
    #for testing
#    list_layer[0].DiameterCurve(output_folder+this_sheet_name+'\层\\')
#    list_hole[0].DiameterCurve(output_folder+this_sheet_name+'\孔\\')
#        
#    list_hole[0].DiameterCurveBatch(output_folder+this_sheet_name+'\孔集合\\') 
#    
#    list_range_hole[0].DiameterCurve(output_folder+this_sheet_name+'\孔划分\\')  
#    list_range_layer[0].DiameterCurve(output_folder+this_sheet_name+'\层划分\\')
#    
#    list_range_hole[0].DiameterCurveBatch(output_folder+this_sheet_name+'\孔划分集合\\')  
#    list_range_layer[0].DiameterCurveBatch(output_folder+this_sheet_name+'\层划分集合\\')
    