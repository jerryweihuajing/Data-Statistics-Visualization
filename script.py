# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:43:10 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

from __init__ import *


#merge xls
list_merged_xls_name=['颗分.xls','颗分2.xls','颗分3.xls']

#construct list xls path
list_merged_xls_path=['.\Data\\input\\'+this_xls_name for this_xls_name in list_merged_xls_name]

#ES.MergedWorkbookStatistics(list_merged_xls_path,3,2)
SC.MergedWorkbookClassification(list_merged_xls_path,3,2)      

#batch processing
BP.Go('.\Data\\input\\',3,2)