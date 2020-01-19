# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 20:47:26 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Module-Stastics of Resilience Curve
"""

import xlrd,xlwt
import numpy as np
import pandas as pd

import operation_head_column as O_H_C
import operation_list as O_L
import operation_path as O_P

from o_data import data
    
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
def WorkbookResilience(xls_path,num_head_rows,num_head_columns):
    
    print('')
    print('--Workbook Resilience')
    
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
            
        index_list=[0,
                    1,
                    2,
                    3,
                    index_index_compression,
                    index_index_resilience,
                    index_porosity_original,
                    index_pressure_consolidation]
        
        #indoor id, hole id, start depth, end depth, 
        #pore aperture, consolidation pressure, compression index, resilience index
        list_indoor_id,\
        list_hole_id,\
        list_start_depth,\
        list_end_depth,\
        list_index_compression,\
        list_index_resilience,\
        list_porosity_original,\
        list_pressure_consolidation=[O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid) for this_index in index_list]
        
        #settlement volume
        list_index=[index_settlement_compression,
                    index_settlement_resilience,
                    index_settlement_recompression]
        
        list_data=[]
        
        for this_index_list in list_index:
            
            #matrix to contain grain partition proportion    
            this_data=np.zeros((len(index_valid),len(this_index_list)))
            
            column=0
                
            for this_index in this_index_list:
                
                this_data[:,column]=O_L.CustomIndexList(list(value_matrix[num_head_rows:,this_index]),index_valid)
            
                column+=1
                
            list_data.append(this_data)
        
        data_settlement_compression,\
        data_settlement_resilience,\
        data_settlement_recompression=list_data
        
        #construct data object
        for i in range(len(index_valid)):
            
            that_data=data()
            
            that_data.hole_id=list_hole_id[i]
            that_data.indoor_id=list_indoor_id[i]
            that_data.end_depth=list_end_depth[i]
            that_data.start_depth=list_start_depth[i]
            that_data.porosity_original=list_porosity_original[i]
            that_data.pressure_consolidation=list_pressure_consolidation[i]
            that_data.index_compression=list_index_compression[i]
            that_data.index_resilience=list_index_resilience[i]
            
            print('')
            print('...')
            print('......')
            print('Hole ID:',that_data.hole_id)
            
            '''calculate a and e of compression'''
            that_data.pressure_compression=pressure_compression
            that_data.settlement_compression=data_settlement_compression[i]
                   
            #difference of s and p
            diff_p=np.array(that_data.pressure_compression[1:])\
                  -np.array(that_data.pressure_compression[:-1])
        
            diff_s=np.array(that_data.settlement_compression[1:])\
                  -np.array(that_data.settlement_compression[:-1])
                          
            #first value
            s_0=that_data.settlement_compression[0]
            p_0=that_data.pressure_compression[0]
            e_0=that_data.porosity_original
            
            '''unit of compression coeffient is 1/MPa'''
            a_0=(s_0/p_0)*1000/20*(1+e_0)
            
            list_a=[a_0]+list((diff_s/diff_p)*1000/20*(1+e_0))
            list_diff_p=[p_0]+list(diff_p.ravel())
        
            #porosity list
            list_e=[e_0]
            
            for j in range(len(list_a)):
                
                e_next=list_e[j]-list_a[j]*list_diff_p[j]/1000
                
#                        print('...')
#                        print('last e:',list_e[j])
#                        print('a:',list_a[j])
#                        print('diff p:',list_diff_p[j])
#                        print('next e:',e_next)
#                
                list_e.append(e_next)
        
            that_data.coefficient_compression=list_a
            that_data.porosity_compression=list_e

#            print(that_data.pressure_compression)
#            print(that_data.porosity_compression)
            
            #compression modulus calculation
            a=that_data.coefficient_compression[that_data.pressure_compression.index(200)]
            
            that_data.modulus_compression=(1+e_0)/a
            
            """e=e0-(1+e0)ΔH/20"""
            
            '''calculate a and e of resilience'''
            that_data.pressure_resilience=[800]+pressure_resilience
            that_data.settlement_resilience=data_settlement_resilience[i]
            
            that_data.porosity_resilience=list(e_0-(1+e_0)*np.array(that_data.settlement_resilience)/20)
            
            #tail: add an element whose pressure is 800
            e_800=that_data.porosity_compression[that_data.pressure_compression.index(800)+1]

            that_data.porosity_resilience.insert(0,e_800)
            
#            print(that_data.pressure_resilience)
#            print(that_data.porosity_resilience)
            
            #resilience modulus calculation
            s_100=that_data.settlement_resilience[that_data.pressure_resilience.index(100)]
            s_200=that_data.settlement_resilience[that_data.pressure_resilience.index(200)]

            that_data.modulus_resilience=(200-100)/(s_200-s_100)/1000*20
            
            '''calculate a and e of recompression'''
            that_data.pressure_recompression=[50]+pressure_recompression+[1600]
            that_data.settlement_recompression=data_settlement_recompression[i]
        
            that_data.porosity_recompression=list(e_0-(1+e_0)*np.array(that_data.settlement_recompression)/20)
        
            #head: add an element whose pressure is 50
            e_50=that_data.porosity_resilience[-1]
#            
            that_data.porosity_recompression.insert(0,e_50)
            
            #tail: add an element whose pressure is 1600
            e_1600=that_data.porosity_compression[that_data.pressure_compression.index(1600)+1]

            that_data.porosity_recompression.append(e_1600)

#            print(that_data.pressure_recompression)
#            print(that_data.porosity_recompression)
                  
            print('Pc: %dkPa'%(that_data.pressure_consolidation))
            print('Cc: %.3f'%(that_data.index_compression))
            print('Cs: %.3f'%(that_data.index_resilience))
            print('Es1-2: %.2fMPa'%(that_data.modulus_compression))
            print('Eo2-1: %.2fMPa'%(that_data.modulus_resilience))

            '''print all data in sample paper'''
            new_sheet.write(i*7+1,0,'室内编号',style)
            new_sheet.write(i*7+1,1,that_data.indoor_id,style)
            new_sheet.write(i*7+1,2,'野外编号',style)
            new_sheet.write(i*7+1,3,that_data.hole_id,style)
            new_sheet.write(i*7+1,4,'起始深度',style)
            new_sheet.write(i*7+1,5,str(that_data.start_depth)+'m',style)
            new_sheet.write(i*7+1,6,'终止深度',style)
            new_sheet.write(i*7+1,7,str(that_data.end_depth)+'m',style)
            
            new_sheet.write(i*7+2,0,'先期固结压力',style)
            new_sheet.write(i*7+2,1,'Pc=%dkPa'%(that_data.pressure_consolidation),style)
            new_sheet.write(i*7+2,2,'压缩指数',style)
            new_sheet.write(i*7+2,3,'Cc=%.3f'%(that_data.index_compression),style)
            new_sheet.write(i*7+2,4,'回弹指数',style)
            new_sheet.write(i*7+2,5,'Cs=%.3f'%(that_data.index_resilience),style)
            new_sheet.write(i*7+2,6,'压缩模量',style)
            new_sheet.write(i*7+2,7,'Es1-2=%.2fMPa'%(that_data.modulus_compression),style)
            new_sheet.write(i*7+2,8,'回弹模量',style)
            new_sheet.write(i*7+2,9,'Eo2-1=%.2fMPa'%(that_data.modulus_resilience),style)
            
            new_sheet.write(i*7+3,0,'P (kPa)',style)
            new_sheet.write(i*7+3,1,'0',style)
            
            for j in range(len(that_data.pressure_compression)):
                
                new_sheet.write(i*7+3,j+2,'%d'%(that_data.pressure_compression[j]),style)
               
            new_sheet.write(i*7+4,0,'ΔH (mm)',style)
            new_sheet.write(i*7+4,1,'',style)
            
            for j in range(len(that_data.settlement_compression)):
                
                new_sheet.write(i*7+4,j+2,'%.3f'%(that_data.settlement_compression[j]),style)
               
            new_sheet.write(i*7+5,0,'e',style)
            
            for j in range(len(that_data.porosity_compression)):
                
                new_sheet.write(i*7+5,j+1,'%.3f'%(that_data.porosity_compression[j]),style)
                
            new_sheet.write(i*7+6,0,'a (1/MPa)',style)
            new_sheet.write(i*7+6,1,'',style)
            
            for j in range(len(that_data.coefficient_compression)):
                
                new_sheet.write(i*7+6,j+2,'%.3f'%(that_data.coefficient_compression[j]),style)

            that_data.ResilienceCurve(output_folder)
            
    new_workbook.save(output_folder+'数据输出.xls')