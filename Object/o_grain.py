# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 18:08:07 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Object-grain
"""

import numpy as np

#==============================================================================
#grain object
#============================================================================== 
class grain:
    
    def __init__(self,
                 silt_type=None,
                 fine_grained_type=None,
                 fine_grained_proportion=None,
                 partition_type=None,
                 classification_code=None,
                 classification_type=None,
                 map_diameter_proportion=None,
                 map_partition_proportion=None):
    
        self.silt_type=silt_type
        self.fine_grained_type=fine_grained_type
        self.fine_grained_proportion=fine_grained_proportion
        self.partition_type=partition_type  
        self.classification_code=classification_code
        self.classification_type=classification_type
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
    
            if np.isnan(list_proportion[k]):
                
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
        self.map_partition_proportion=dict(zip(list_partition,list_proportion))
        
        #give value
        self.map_partition_proportion['巨粒-漂石（块石）粒']=self.map_diameter_proportion['>200']
        self.map_partition_proportion['巨粒-卵石（碎石）粒']=self.map_diameter_proportion['20-200']*7/9
        self.map_partition_proportion['粗粒-砾粒粗砾']=self.map_diameter_proportion['20-200']*2/9
        self.map_partition_proportion['粗粒-细砾']=self.map_diameter_proportion['2-20']
        self.map_partition_proportion['粗粒-砂砾']=self.map_diameter_proportion['0.5-2']\
                                            +self.map_diameter_proportion['0.25-0.5']\
                                            +self.map_diameter_proportion['0.075-0.25']
        self.map_partition_proportion['细粒-粉粒']=self.map_diameter_proportion['0.005-0.05']
        self.map_partition_proportion['细粒-黏粒']=self.map_diameter_proportion['<0.005']
        
#        print(self.map_partition_proportion)
        
        #grain partition result
        self.partition_type=DictKeyOfValue(self.map_partition_proportion,max(list(self.map_partition_proportion.values())))

#        print(self.partition_type)
      
    def Classification(self,Cu,Ce):
        
        #calculate proportion of fine grained
        self.fine_grained_proportion=self.map_partition_proportion['细粒-粉粒']+self.map_partition_proportion['细粒-粘土粒']
        
        #calculate type of fine grained
        map_to_decide_type=DictSlice(self.map_partition_proportion,-2,len(self.map_partition_proportion))
        
        #decide fine grained type
        self.fine_grained_type=DictKeyOfValue(map_to_decide_type,max(list(map_to_decide_type.values())))
        
#        print(self.fine_grained_type,self.fine_grained_proportion)
        
        #init
        self.classification_code=''
        self.classification_type=''
        
        #considering grain proportion
        if self.fine_grained_proportion<5:
            
            if Cu>=5 and 1<=Ce<=3:
                
                self.classification_code='W'
                self.classification_type='级配良好'
                
            else:
                
                self.classification_code='P'
                self.classification_type='级配不良'
                
        if 5<=self.fine_grained_proportion<=15: 
            
            self.classification_code='F'
            self.classification_type='含细粒土'
            
        if 15<self.fine_grained_proportion<=50: 
            
            if '黏' in self.fine_grained_type:
                
                self.classification_code='C'
                self.classification_type='黏土质'
            
            if '粉' in self.fine_grained_type:
                
                self.classification_code='M'
                self.classification_type='粉土质'
            
        if not isinstance(self.silt_type,str):
            
            self.silt_type='其他'
            
        #exception
        if self.classification_code!='' and self.classification_type!='':
            
            if '砾' in self.silt_type:
                
                self.classification_code='G'+self.classification_code
                self.classification_type+='砾'
                
            elif '砂' in self.silt_type:
                
                self.classification_code='S'+self.classification_code
                self.classification_type+='砂'
            
            else:
                
                self.classification_code='others'
                self.classification_type='其他'
                
        if self.classification_code=='' and self.classification_type=='':
            
            self.classification_code='others'
            self.classification_type='其他'
            
#        print(self.classification_code,self.classification_type)
        