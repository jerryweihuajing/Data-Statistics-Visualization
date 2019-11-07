# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:43:10 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

from __init__ import *

xls_path='.\Data\\input\\土工试验54个.xls'

DF.SheetsFiltering(xls_path,3)

#ES.WorkbookStatistics(xls_path,3,2)    
#SC.WorkbookClassification(xls_path,3,2)           

#folder_path='.\Data\\input\\'
#
#BP.Go(folder_path,3,2)

