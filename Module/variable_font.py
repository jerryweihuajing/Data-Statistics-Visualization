# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:38:21 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Variable-Font
"""

from matplotlib.font_manager import FontProperties

#sample data font
sample_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=10)
    
#title font
annotation_font=FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=16)

#annotation font
title_font=FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=20)

#legned prop
legend_prop={'family':'Gill Sans MT','weight':'normal','size':12}