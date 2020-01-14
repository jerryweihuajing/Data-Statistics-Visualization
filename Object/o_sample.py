# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:53:54 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Object-sample
"""

#==============================================================================
#scatter sample
#==============================================================================    
class sample:
    def __init__(self,
                 pos_x=None,
                 pos_y=None,
                 pos_annotation=None):
        
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.pos_annotation=pos_annotation
