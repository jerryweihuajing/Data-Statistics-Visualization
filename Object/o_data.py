# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 20:41:47 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Object-data
"""

from o_sample import sample

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

import operation_list as O_L
import calculation_numerical_analysis as C_N_A
import calculation_pressure_consolidation as C_P_C

#sample data font
sample_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=9)
    
#title font
annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)

#annotation font
title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)
    
#==============================================================================
#object to store and operate data
#==============================================================================    
class data:
    def __init__(self,
                 list_data=None,
                 indoor_id=None,
                 hole_id=None,
                 start_depth=None,
                 end_depth=None,
                 pressure_consolidation=None,
                 index_compression=None,
                 index_resilience=None,
                 modulus_compression=None,
                 modulus_resilience=None,
                 porosity_original=None,
                 porosity_compression=None,
                 porosity_resilience=None,
                 porosity_recompression=None,
                 coefficient_compression=None,
                 coefficient_resilience=None,
                 coefficient_recompression=None,
                 pressure_compression=None,
                 pressure_resilience=None,
                 pressure_recompression=None,
                 settlement_compression=None,
                 settlement_resilience=None,
                 settlement_recompression=None,
                 valid_logP_compression=None,
                 valid_logP_resilience=None,
                 valid_logP_recompression=None,
                 valid_e_compression=None,
                 valid_e_resilience=None,
                 valid_e_recompression=None,
                 list_diameter=None,
                 list_diameter_lg=None,
                 list_diameter_percentage=None,
                 list_diameter_percentage_cumulative=None):
        
        self.list_data=list_data
        
        #basic information
        self.indoor_id=indoor_id
        self.hole_id=hole_id
        self.start_depth=start_depth
        self.end_depth=end_depth
        self.porosity_original=porosity_original
        self.pressure_consolidation=pressure_consolidation
        
        #index 
        self.index_compression=index_compression
        self.index_resilience=index_resilience
        
        #modulus
        self.modulus_compression=modulus_compression
        self.modulus_resilience=modulus_resilience
                 
        #coefficient
        self.coefficient_compression=coefficient_compression
        self.coefficient_resilience=coefficient_resilience
        self.coefficient_recompression=coefficient_recompression
        
        #pressure
        self.pressure_compression=pressure_compression
        self.pressure_resilience=pressure_resilience
        self.pressure_recompression=pressure_recompression
        
        #porosity
        self.porosity_compression=porosity_compression
        self.porosity_resilience=porosity_resilience
        self.porosity_recompression=porosity_recompression
        
        #settlement volume
        self.settlement_compression=settlement_compression
        self.settlement_resilience=settlement_resilience
        self.settlement_recompression=settlement_recompression
        
        #data for visualization
        #log10 of pressure
        self.valid_logP_compression=valid_logP_compression
        self.valid_logP_resilience=valid_logP_resilience
        self.valid_logP_recompression=valid_logP_recompression
        
        #porosity
        self.valid_e_compression=valid_e_compression
        self.valid_e_resilience=valid_e_resilience
        self.valid_e_recompression=valid_e_recompression
    
        #for diameter curve
        self.list_diameter=list_diameter
        self.list_diameter_log2=list_diameter_lg
        self.list_diameter_percentage=list_diameter_percentage
        self.list_diameter_percentage_cumulative=list_diameter_percentage_cumulative
        
    def PerfectDataVisualization(self,x_step,y_step):
    
        #scatter data
        x_compression=self.valid_logP_compression
        y_compression=self.valid_e_compression
        
        x_resilience=self.valid_logP_resilience
        y_resilience=self.valid_e_resilience
        
        x_recompression=self.valid_logP_recompression
        y_recompression=self.valid_e_recompression
        
        #result of interpolation
        new_x_y_compression=C_N_A.LargrangeInterpolation(x_compression,y_compression)
        new_x_y_resilience=C_N_A.LargrangeInterpolation(x_resilience,y_resilience)
        new_x_y_recompression=C_N_A.LargrangeInterpolation(x_recompression,y_recompression)
        
        new_x_compression=[this_x_y[0] for this_x_y in new_x_y_compression]
        new_y_compression=[this_x_y[1] for this_x_y in new_x_y_compression]
        
        new_x_resilience=[this_x_y[0] for this_x_y in new_x_y_resilience]
        new_y_resilience=[this_x_y[1] for this_x_y in new_x_y_resilience]
        
        new_x_recompression=[this_x_y[0] for this_x_y in new_x_y_recompression]
        new_y_recompression=[this_x_y[1] for this_x_y in new_x_y_recompression]
        
        #plot curve
        plt.plot(new_x_compression,new_y_compression,'grey')
        plt.plot(new_x_resilience,new_y_resilience,'grey')
        plt.plot(new_x_recompression,new_y_recompression,'grey')
        
        #construct sample list
        samples_compression=O_L.SampleList(x_compression,y_compression)
        samples_resilience=O_L.SampleList(x_resilience,y_resilience)
        samples_recompression=O_L.SampleList(x_recompression,y_recompression)

        '''init'''
        for this_sample in samples_compression+samples_resilience+samples_recompression:
            
            this_sample.pos_annotation='lower'
            
        '''resilience and recompression comparison'''
        for this_sample in samples_resilience:
            
            for that_sample in samples_recompression:
                
                #compare y coordinates
                if this_sample.pos_x==that_sample.pos_x:
                    
                    if '%.3f'%this_sample.pos_y<'%.3f'%that_sample.pos_y:
        
                        that_sample.pos_annotation='upper'
                        
                    if '%.3f'%this_sample.pos_y>'%.3f'%that_sample.pos_y:
        
                        this_sample.pos_annotation='upper'
                        
        '''delete samples of being stacked'''
        for this_sample in samples_resilience+samples_recompression:
            
            for that_sample in samples_compression:              
                
                if '%d'%(100**this_sample.pos_x)=='%d'%(100**that_sample.pos_x):
                    
                    if '%.3f'%this_sample.pos_y=='%.3f'%that_sample.pos_y:

                        this_sample.pos_annotation='None'
                    
        #plot sample data
        for this_sample in samples_compression+samples_resilience+samples_recompression:

            if this_sample.pos_annotation!='None':
    
                if this_sample.pos_annotation=='upper':
                    
                    factor=0.2
                    
                if this_sample.pos_annotation=='lower':
                    
                    factor=-0.3   
                    
                plt.scatter(this_sample.pos_x,this_sample.pos_y,color='k')
    
                plt.annotate('(%d,%.3f)'%(np.round(10**this_sample.pos_x),this_sample.pos_y),
                             xy=(this_sample.pos_x,this_sample.pos_y),
                             xytext=(this_sample.pos_x-0.5*x_step,
                                     this_sample.pos_y+factor*y_step),
                             color='k',
                             fontproperties=sample_font)
     
    def ResilienceCurve(self,output_folder):
        
        #delete the first element
        valid_P_compression=self.pressure_compression
        valid_e_compression=self.porosity_compression[1:]
        valid_P_resilience=self.pressure_resilience
        valid_e_resilience=self.porosity_resilience
        valid_P_recompression=self.pressure_recompression
        valid_e_recompression=self.porosity_recompression
        
        if valid_P_compression==[]\
        or valid_e_compression==[]\
        or valid_P_resilience==[]\
        or valid_e_resilience==[]\
        or valid_P_recompression==[]\
        or valid_e_recompression==[]:
            
            return None
        
        #Logarithm of P
        valid_logP_compression=[np.log10(item) for item in valid_P_compression]
        valid_logP_resilience=[np.log10(item) for item in valid_P_resilience]
        valid_logP_recompression=[np.log10(item) for item in valid_P_recompression]
        
        #combine all variabls
        valid_logP=valid_logP_compression
        valid_e=list(valid_e_compression)+list(valid_e_resilience)+list(valid_e_recompression)
        
        '''canvas'''
        fig,ax=plt.subplots(figsize=(8,8))
        
        #calculation of consolidation pressure
        final_Pc=C_P_C.CalculatePcAndCc(valid_logP_compression,valid_e_compression,show=1)  
        
        #set ticks
        plt.tick_params(labelsize=12)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        
        plt.title('ID: '+str(self.hole_id),FontProperties=title_font)  
                
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
        
        #set locator
        ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
        
        #init data for visualization
        self.valid_logP_compression=valid_logP_compression
        self.valid_e_compression=valid_e_compression
        self.valid_logP_resilience=valid_logP_resilience
        self.valid_e_resilience=valid_e_resilience
        self.valid_logP_recompression=valid_logP_recompression
        self.valid_e_recompression=valid_e_recompression
        
        '''visualization of curve'''
        self.PerfectDataVisualization(x_major_step,y_major_step)
        
        #visualization of curve
#        C_P_C.DataVisualization(valid_logP_compression,
#                                valid_e_compression,
#                                x_major_step,
#                                y_major_step)
#        
#        C_P_C.DataVisualization(valid_logP_resilience,
#                                valid_e_resilience,
#                                x_major_step,
#                                y_major_step)
#        
#        C_P_C.DataVisualization(valid_logP_recompression,
#                                valid_e_recompression,
#                                x_major_step,
#                                y_major_step)
#        
        #add depth
        plt.text(0.95*np.average(valid_logP),max(valid_e),
                 'Start Depth: '+str(self.start_depth)+'m End Depth: '+str(self.end_depth)+'m',
                 FontProperties=annotation_font)
        
        #show the grid
        plt.grid()
        plt.show()
    
        fig_path=output_folder+str(self.hole_id)+'.png'
        
        #save the fig
        plt.savefig(fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
        return final_Pc
    
    def ConsolidationCurve(self,output_folder):
        
        #delete the first element
        valid_P_compression=self.pressure_compression[1:]
        valid_e_compression=self.porosity_compression[1:]
        
        if valid_P_compression==[]\
        or valid_e_compression==[]:
            
            return None
        
        #Logarithm of P
        valid_logP_compression=[np.log10(item) for item in valid_P_compression]
        
        #combine all variabls
        valid_logP=valid_logP_compression
        valid_e=list(valid_e_compression)
        
        '''canvas'''
        fig,ax=plt.subplots(figsize=(8,8))
        
        #calculation of consolidation pressure
        final_Pc=C_P_C.CalculatePcAndCc(valid_logP_compression,valid_e_compression,show=1)  
        
        #set ticks
        plt.tick_params(labelsize=12)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        
        #title font
        annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)
        
        #annotation font
        title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)
        
        plt.title('ID: '+str(self.hole_id),FontProperties=title_font)  
                
        plt.xlabel('lgP',FontProperties=annotation_font)
        plt.ylabel('e',FontProperties=annotation_font)
        
        #label fonts
        for this_label in labels:
            
            this_label.set_fontname('Times New Roman')
            
        #tick step
        x_major_step=(max(valid_logP)-min(valid_logP))/10
        x_minor_step=x_major_step/2
        y_major_step=(max(valid_e)-min(valid_e))/10
        y_minor_step=y_major_step/2
        
        #set locator
        ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
        
        #visualization of curve
        C_P_C.DataVisualization(valid_logP_compression,
                                valid_e_compression,
                                x_major_step,
                                y_major_step,
                                True)
        
        #add depth
        plt.text(0.95*np.average(valid_logP),max(valid_e),
                 'Start Depth: '+str(self.start_depth)+'m End Depth: '+str(self.end_depth)+'m',
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
            
        fig_path=output_folder+str(self.hole_id)+'.png'
        
        #save the fig
        plt.savefig(fig_path,dpi=300,bbox_inches='tight')
        plt.close()
    
        return final_Pc
    
    def DiameterCurve(self,output_folder):
        
        '''canvas'''
        fig,ax=plt.subplots(figsize=(8,6))
        
        #set ticks
        plt.tick_params(labelsize=12)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        
        plt.title('ID: '+str(self.hole_id),FontProperties=title_font)  
                
        plt.xlabel('lg of Diameter(lg(mm))',FontProperties=annotation_font)
        plt.ylabel('Percentage(%)',FontProperties=annotation_font)
        
        #label fonts
        for this_label in labels:
            
            this_label.set_fontname('Times New Roman')
                
        x_alias=[k for k in range(len(self.list_diameter_percentage_cumulative))]
        y_alias=np.copy(self.list_diameter_percentage_cumulative)
        
        #diameter list in lg form
        self.list_diameter_lg=[np.round(np.log10(item),3) for item in self.list_diameter[:-1]]+[0.00]
        
        valid_x=x_alias
        valid_y=[int(np.round(item*10))/10 for item in y_alias]
        
        #tick step
        x_major_step=1
        x_minor_step=0.5
        y_major_step=10
        y_minor_step=5
    
        #set locator
        ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))

        '''fitting respectively'''
        index_separation=list(valid_y).index(np.max([item for item in list(valid_y) if item<100]))

#        print('y alias:',y_alias)
        
        #smoothing the curve
        X=valid_x[index_separation-1:]
        Y=valid_y[index_separation-1:]

        '''p-chip interpolation'''
        smoothed_x_y=C_N_A.PChipInterpolation(X,Y)

        x_smoothed=[this_x_y[0] for this_x_y in smoothed_x_y]
        y_smoothed=[this_x_y[1] for this_x_y in smoothed_x_y]
        
        plt.plot(x_smoothed,y_smoothed,'grey')

#        '''line'''
#        plt.plot(x_alias[:index_separation],y_alias[:index_separation],'grey')
        
        #set the interval manually
        '''represent A with B'''
        plt.xticks([item+0.5 for item in x_alias],self.list_diameter_lg)
        
        plt.xlim([x_alias[index_separation-1]-x_minor_step,x_alias[-1]+x_minor_step])
        plt.ylim([0-y_minor_step,100+y_minor_step])
        
        samples=[]

        for t in range(len(valid_x)):
            
            if t<index_separation-1:
                
                continue
            
            new_sample=sample()
            
            new_sample.pos_x=valid_x[t]
            new_sample.pos_y=valid_y[t]
            
            samples.append(new_sample)
                  
        #plot sample data
        for this_sample in samples:
    
            if np.isnan(this_sample.pos_y):
                
                continue
    
            plt.scatter(this_sample.pos_x,this_sample.pos_y,color='k')
    
            plt.annotate('%.1f%%'%this_sample.pos_y,
                         xy=(this_sample.pos_x+0.1,
                             this_sample.pos_y),
                         xytext=(this_sample.pos_x+0.1*x_major_step,
                                 this_sample.pos_y+0.1*y_major_step),
                         color='k',
                         fontproperties=sample_font)
       
        #add depth
        plt.text(x_alias[index_separation-1],0,
                 'Start Depth: '+str(self.start_depth)+'m End Depth: '+str(self.end_depth)+'m',
                 FontProperties=annotation_font)
        
        #show the grid
        plt.grid()
        plt.show()
        
        fig_path=output_folder+str(self.hole_id)+'.png'
        
        #save the fig
        plt.savefig(fig_path,dpi=300,bbox_inches='tight')
        plt.close()
        
    def DiameterCurveBatch(self,output_folder):
        
        '''canvas'''
        fig,ax=plt.subplots(figsize=(8,6))
        
        #set ticks
        plt.tick_params(labelsize=12)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        
        plt.title('ID: '+str(self.hole_id),FontProperties=title_font)  
                
        plt.xlabel('lg of Diameter(lg(mm))',FontProperties=annotation_font)
        plt.ylabel('Percentage(%)',FontProperties=annotation_font)
        
        #label fonts
        for this_label in labels:
            
            this_label.set_fontname('Times New Roman')
            
        #tick step
        x_major_step=1
        x_minor_step=0.5
        y_major_step=10
        y_minor_step=5
    
        #set locator
        ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))    
        
        list_index_separation=[]
        
        #diameter list in lg form
        self.list_diameter_lg=[np.round(np.log10(item),3) for item in self.list_diameter]
        
        for this_data in self.list_data:
            
            x_alias=[k for k in range(len(this_data.list_diameter_percentage_cumulative))]
            y_alias=np.copy(this_data.list_diameter_percentage_cumulative)
            
            valid_x=x_alias
            valid_y=[int(np.round(item*10))/10 for item in y_alias]
                
            '''fitting respectively'''
            index_separation=list(valid_y).index(np.max([item for item in list(valid_y) if item<100]))
        
            #collect it
            list_index_separation.append(index_separation)
            
        #        print('y alias:',y_alias)
            
            #smoothing the curve
            X=valid_x[index_separation-1:]
            Y=valid_y[index_separation-1:]
        
            '''p-chip interpolation'''
            smoothed_x_y=C_N_A.PChipInterpolation(X,Y)
        
            x_smoothed=[this_x_y[0] for this_x_y in smoothed_x_y]
            y_smoothed=[this_x_y[1] for this_x_y in smoothed_x_y]
            
            plt.plot(x_smoothed,y_smoothed,'grey')
        
        #        '''line'''
        #        plt.plot(x_alias[:index_separation],y_alias[:index_separation],'grey')
        
            samples=[]
        
            for t in range(len(valid_x)):
                
                if t<index_separation-1:
                    
                    continue
                
                new_sample=sample()
                
                new_sample.pos_x=valid_x[t]
                new_sample.pos_y=valid_y[t]
                
                samples.append(new_sample)
                      
            #plot sample data
            for this_sample in samples:
        
                if np.isnan(this_sample.pos_y):
                    
                    continue
        
                plt.scatter(this_sample.pos_x,this_sample.pos_y,color='k')
        
                '''it is in a mess for mass of data'''
#                plt.annotate('%.1f%%'%this_sample.pos_y,
#                             xy=(this_sample.pos_x+0.1,
#                                 this_sample.pos_y),
#                             xytext=(this_sample.pos_x+0.1*x_major_step,
#                                     this_sample.pos_y+0.1*y_major_step),
#                             color='k',
#                             fontproperties=sample_font)
                                       
        #set the interval manually
        '''represent A with B'''
        plt.xticks([item+0.5 for item in x_alias],self.list_diameter_lg)
        
        plt.xlim([x_alias[np.min(list_index_separation)-1]-x_minor_step,x_alias[-1]+x_minor_step])
        plt.ylim([0-y_minor_step,100+y_minor_step])
            
        #add depth
        plt.text(x_alias[np.min(list_index_separation)-1],0,
                 'Start Depth: '+str(self.start_depth)+'m End Depth: '+str(self.end_depth)+'m',
                 FontProperties=annotation_font)
        
        #show the grid
        plt.grid()
        plt.show()
        
        fig_path=output_folder+str(self.hole_id)+'.png'
        
        #save the fig
        plt.savefig(fig_path,dpi=300,bbox_inches='tight')
        plt.close()