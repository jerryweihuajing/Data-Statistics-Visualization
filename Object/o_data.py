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

import PcCalculation as PC

#==============================================================================
#object to store and operate data
#==============================================================================    
class data:
    
    def __init__(self,
                 hole_id=None,
                 start_depth=None,
                 end_depth=None,
                 e0=None,
                 alpha=None,
                 P_pressure=None,
                 e_pressure=None,
                 P_resiliance=None,
                 e_resiliance=None,
                 P_recompress=None,
                 e_recompress=None):
        
        self.hole_id=hole_id
        start_depth=start_depth
        end_depth=end_depth
        e0=e0
        alpha=alpha
        P_pressure=P_pressure
        e_pressure=e_pressure
        P_resiliance=P_resiliance
        e_resiliance=e_resiliance
        P_recompress=P_recompress
        e_recompress=e_recompress
        
    def Canvas(self,output_folder):
        
        #delete the first element
        valid_P_pressure=self.P_pressure[1:]
        valid_e_pressure=self.e_pressure[1:]
        valid_P_resiliance=self.P_resiliance[1:]
        valid_e_resiliance=self.e_resiliance[1:]
        valid_P_recompress=self.P_recompress[1:]
        valid_e_recompress=self.e_recompress[1:]
        
        if valid_P_pressure==[]\
        or valid_e_pressure==[]\
        or valid_P_resiliance==[]\
        or valid_e_resiliance==[]\
        or valid_P_recompress==[]\
        or valid_e_recompress==[]:
            
            return None
        
        #Logarithm of P
        valid_logP_pressure=[np.log10(item) for item in valid_P_pressure]
        valid_logP_resiliance=[np.log10(item) for item in valid_P_resiliance]
        valid_logP_recompress=[np.log10(item) for item in valid_P_recompress]
        
        #combine all variabls
        valid_logP=valid_logP_pressure+valid_logP_resiliance+valid_logP_recompress
        valid_e=list(valid_e_pressure)+list(valid_e_resiliance)+list(valid_e_recompress)
        
        '''canvas'''
        fig,ax=plt.subplots(figsize=(8,8))
        
        final_Pc=PC.CalculatePcAndCc(valid_logP_pressure,valid_e_pressure,show=1)  

        #set ticks
        plt.tick_params(labelsize=12)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        
        #title font
        annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)
        
        #annotation font
        title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)
        
        plt.title('ID:'+str(self.hole_id),FontProperties=title_font)  
                
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
        
        #add depth
        plt.text(np.average(valid_logP),max(valid_e),
                 'Start Depth:'+str(self.start_depth)+'m End Depth:'+str(self.end_depth)+'m',
                 FontProperties=annotation_font)
        
        #show the grid
        plt.grid()
        plt.show()
    
        #save the fig    
        plt.savefig(output_folder+str(self.hole_id)+'.png')   
        plt.close()
        
        return final_Pc