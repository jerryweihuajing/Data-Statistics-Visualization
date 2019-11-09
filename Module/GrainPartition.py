# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:44:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Grain Partition
"""

#------------------------------------------------------------------------------
"""
The dictionary searches for key by value

Args:
    which_dictionary: the dictionary which will be searched
    which_value: target value
    
Returns:
    key for which is searched
"""
def DictKeyOfValue(dictionary,value):
    
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    
    return keys[values.index(value)]

#==============================================================================
#grain object
#============================================================================== 
class grain:
    
    def __init__(self,
                 partition=None,
                 map_diameter_proportion=None,
                 map_partition_proportion=None):
    
        self.partition=partition
        self.map_diameter_proportion=map_diameter_proportion
        self.map_partition_proportion=map_partition_proportion
        
    def InitMap(self,list_proportion):
        
        list_diameter=['>200',\
                       '20-200',\
                       '2-20',\
                       '0.5-2',\
                       '0.25-0.5',\
                       '0.075-0.25',\
                       '0.05-0.075',\
                       '0.005-0.05',\
                       '<0.005']
        
        for k in range(len(list_proportion)):
            
            if list_proportion[k]=='':
                
                list_proportion[k]=0
    
        #construct map between diameter and proportion
        self.map_diameter_proportion=dict(zip(list_diameter,list_proportion))

    def Partition(self):
        
        list_partition=['巨粒-漂石（块石）粒',\
                        '巨粒-卵石（碎石）粒'\
                        '粗粒-砾粒粗砾',\
                        '粗粒-细砾',\
                        '粗粒-砂砾',\
                        '细粒-粉粒',\
                        '细粒-粘土粒']
    
        list_proportion=[0]*len(list_partition)
        
        #construct map between partition and proportion
        map_partition_proportion=dict(zip(list_partition,list_proportion))
        
        #give value
        map_partition_proportion['巨粒-漂石（块石）粒']=self.map_diameter_proportion['>200']
        map_partition_proportion['巨粒-卵石（碎石）粒']=self.map_diameter_proportion['20-200']*7/9
        map_partition_proportion['粗粒-砾粒粗砾']=self.map_diameter_proportion['20-200']*2/9
        map_partition_proportion['粗粒-细砾']=self.map_diameter_proportion['2-20']
        map_partition_proportion['粗粒-砂砾']=self.map_diameter_proportion['0.5-2']\
                                            +self.map_diameter_proportion['0.25-0.5']\
                                            +self.map_diameter_proportion['0.075-0.25']
        map_partition_proportion['细粒-粉粒']=self.map_diameter_proportion['0.005-0.05']
        map_partition_proportion['细粒-粘土粒']=self.map_diameter_proportion['<0.005']
        
        self.partition=DictKeyOfValue(map_partition_proportion,max(list(map_partition_proportion.values())))


list_proportion=['','','','','',42,42,9.7,6.0]

g=grain()

g.InitMap(list_proportion)   
g.Partition()

print(g.partition)
    