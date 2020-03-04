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
sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path))

import statistics_diameter_curve as S_D_C
import statistics_general_variable as S_G_V
import statistics_resilience_curve as S_R_C
import statistics_silt_classification as S_S_C
import statistics_pressure_consolidation as S_P_C
