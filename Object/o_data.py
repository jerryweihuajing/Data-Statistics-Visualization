# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 20:41:47 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Consolidation Calculation
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties


import calculation_pressure_consolidation as C_P_C

#==============================================================================
#object to store and operate data
#==============================================================================    
class data:
    def __init__(self,
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
                 valid_e_recompression=None):
        
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
    
    def PerfectDataVisualization(self,x_step,y_step):
    
        #sample data font
        sammple_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=9)
    
        #scatter data
        x_compression=self.valid_logP_compression
        y_compression=self.valid_e_compression
        
        x_resilience=self.valid_logP_resilience
        y_resilience=self.valid_e_resilience
        
        x_recompression=self.valid_logP_recompression
        y_recompression=self.valid_e_recompression
        
        #result of interpolation
        new_x_y_compression=C_P_C.LargrangeInterpolation(x_compression,y_compression)
        new_x_y_resilience=C_P_C.LargrangeInterpolation(x_resilience,y_resilience)
        new_x_y_recompression=C_P_C.LargrangeInterpolation(x_recompression,y_recompression)
        
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
        
        #plot sample data
        for kk in range(len(x_compression)):
            
             plt.scatter(x_compression[kk],y_compression[kk],color='k')

             plt.annotate('(%d,%.3f)'%(np.round(10**x_compression[kk]),y_compression[kk]),
                          xy=(x_compression[kk],y_compression[kk]),
                          xytext=(x_compression[kk]-0.5*x_step,
                                  y_compression[kk]-0.3*y_step),
                          color='k',
                          fontproperties=sammple_font)
     
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
        x_minor_step=(max(valid_logP)-min(valid_logP))/20
        y_major_step=(max(valid_e)-min(valid_e))/10
        y_minor_step=(max(valid_e)-min(valid_e))/20
        
        #set locator
        ax.xaxis.set_major_locator(MultipleLocator(x_major_step))
        ax.xaxis.set_minor_locator(MultipleLocator(x_minor_step))
        ax.yaxis.set_major_locator(MultipleLocator(y_major_step))
        ax.yaxis.set_minor_locator(MultipleLocator(y_minor_step))
        
        #visualization of curve
        C_P_C.DataVisualization(valid_logP_compression,
                                valid_e_compression,
                                x_major_step,
                                y_major_step)
        
        C_P_C.DataVisualization(valid_logP_resilience,
                                valid_e_resilience,
                                x_major_step,
                                y_major_step)
        
        C_P_C.DataVisualization(valid_logP_recompression,
                                valid_e_recompression,
                                x_major_step,
                                y_major_step)
        
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
        x_minor_step=(max(valid_logP)-min(valid_logP))/20
        y_major_step=(max(valid_e)-min(valid_e))/10
        y_minor_step=(max(valid_e)-min(valid_e))/20
        
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