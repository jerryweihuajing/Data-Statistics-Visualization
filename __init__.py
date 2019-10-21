# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 16:17:21 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：initialization script
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
#sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path))

import HeadColumns as HC
import PathProcessing as PP
import ExcelStatistics as ES
import SiltClassification as SC
