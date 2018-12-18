# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 17:03:13 2018

@author: kh.yuan
"""

import pandas as pd
import re
data=pd.read_csv('test.csv',encoding='ANSI')
data=data.fillna('')
plaintiff=data['原告']
appendix=data['附录']

def PlaintiffChg(text):
    output=[0,0,0,0] #自然人 法人 检察院 其他
    if text=='':
        return output
    
    namelist=text.split('、')
    for name in namelist:
        if not(re.search('公司',name)==None): #检查是否为法人
            output[1]+=1
        elif not(re.search('检察院',name)==None): #检查是否为检察院
            output[2]+=1
        elif not(re.search('厂',name)==None) and len(name)>4: #检查是否为法人
            output[1]+=1
        elif len(name)<=4: #检查是否为自然人。优化算法时可以把这个提到第一个来检查
            output[0]+=1
        else:
            output[3]+=1 #检查是否为其他，一般是外国人或名字中不带公司二字的法人
            print(name)
    return output

def AppendixChg(text):
    output=0
    if text=='':
        return output
    benchmark=['一、','二、','三、','四、','五、','六、','七、','八、','九、','十、','十一、','十二、','十三、','十四、','十五、','十六、','十七、','十八、','十九、','二十、']
    for i in range(0,20):
        if not(re.search(benchmark[i],text)==None):
            output+=1
        else:
            break
    return output