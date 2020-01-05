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
#list_merged_xls_name=['颗分1.xls','颗分2.xls','颗分3.xls','地质调查HAB-1.xls']

#construct list xls path
#list_merged_xls_path=['.\Data\\input\\'+this_xls_name for this_xls_name in list_merged_xls_name]

#ES.MergedWorkbookStatistics(list_merged_xls_path,3,2)
#SC.MergedWorkbookClassification(list_merged_xls_path,3,2)      

#xls_path=os.getcwd()+'\\Data\input\城市地质调查高压数据.xls'
#
#'''better annotation position'''
#S_R_C.WorkbookResilience(xls_path,2,2)

xls_path=os.getcwd()+'\\Data\input\淮安城市地质土工试验54个.xls'

S_G_V.WorkbookStatistics(xls_path,3,2)
S_S_C.WorkbookClassification(xls_path,3,2)

#xls_path=os.getcwd()+'\\Data\input\淮安城市地质有高压数据部分.xls'
#
#S_P_C.WorkbookCondolidation(xls_path,3,2)

