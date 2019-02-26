#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 10:31:13 2018

@author: wujiaxin
"""
import re
import numpy as np
import pandas as pd
#import datetime 
#import os
#import jieba
#import law
#import jieba.posseg as pseg

# State all the possible Hyperparameters you used in this script
file_path = "/Users/wujiaxin/Desktop/crime4.xlsx"
alpha = 10
beta = 10
gamma = 10

# 读取一些数据
data = pd.read_excel(file_path)
data.head()
# 如果你选择了 6 和 14

def number6(data):#判决日期→年、月、日，空值采用None填补
    year=[]#判决年份
    month=[]#判决月份
    day=[]#判决日期
    for x in data['判决日期']:
        #寻找年的字段，如果未找到，使用空值None填补
        a=re.compile(r'.*年')
        b=a.search(str(x))
        if b==None:
            year.append(None)
        else:
            year.append(b.group(0))
            x=re.sub(b.group(0),'',x)#删掉省字段，方便寻找月字段

        #找出月的字段，如果未找到，使用空值None填补
        a1=re.compile(r'.*月')
        b1=a1.search(str(x))
        if b1==None:
            month.append(None)
        else:
            month.append(b1.group(0))
            x=re.sub(b1.group(0),'',x)#删掉省字段，方便寻找日字段

        #找出日的字段，如果未找到，使用空值None填补
        a2=re.compile(r'.*日')
        b2=a2.search(str(x))
        if b2==None:
            day.append(None)
        else:
            day.append(b2.group(0))

    #创建字典，方便创建DataFrame
    newdict={
                '判决年份':year,
                '判决月份':month,
                '判决日期':day
                }
    #通过字典建立DataFrame，并合并
    newdata=pd.DataFrame(newdict)
    data=pd.concat([data,newdata],axis=1)
    return data
   
def find_law_tiao_kuan_in_text(string):
    final_list = []
    # We first find these "< >"
    sign_find = re.compile(r"《.*?》")
    # We use these names to refind the tiaokuan
    law_list = re.findall(sign_find, string)
    law_set = set(law_list)
    law_length = len(law_set)
    #print(law_set)

    if law_length > 0:  # only do the following when the list is not empty

        # We do this because it's hard to match the law and its tiaokuan.
        for j in range(law_length):
            thislaw = law_set.pop()
            #print(thislaw)
            tiao_finder = re.compile(thislaw+r"第.*?条.*?(?:《|。|$)")
            tiao = re.findall(tiao_finder, string)
            #print("tiao",tiao)
            # Notice that there might be same laws many times

            real_tiao_list = []
            kuan_list = []

            if len(tiao) > 0:
                for k in range(len(tiao)):
                    if len(tiao[k])>0:
                        #print(tiao[k].split(','))
                        tiao_finder_plus = re.compile(r"第.{1,5}条") # Assume that no more than 5 between tiao
                        real_tiao = re.findall(tiao_finder_plus, tiao[k])
                        #print("real_tiao",real_tiao)
                        real_tiao_list.extend(real_tiao)
                        
                        for p in range(len(real_tiao)):
                            kuan_finder = re.compile(real_tiao[p]+"第.{1,5}款")
                            kuan = re.findall(kuan_finder,tiao[k])
                            kuan_list.extend(kuan)
                        #print(kuan_list)
            final_list.append([thislaw,real_tiao_list,kuan_list])
    return final_list

def number14(data):
    selected_data=data["判决结果"]
    data_len = len(selected_data)

    basis=[]#判决依据的条款
    result=["N/A"]*data_len#判决结果
    charge=["N/A"]*data_len
    sentence=["N/A"]*data_len

    for i in range(data_len):
        if pd.isnull(selected_data.iloc[i]):
           basis.append([])
           continue
        basis.append(find_law_tiao_kuan_in_text(selected_data.iloc[i]))
    
    #查找判决结果，空缺值用N/A进行填补        
    for i in range(selected_data.shape[0]):     
        if type(selected_data[i]) is not float:
            for j in range(len(selected_data[i])):
                if ("判决" in selected_data[i][j-4:j+4] or "裁定" in selected_data[i][j-4:j+4]) and ("法院" not in selected_data[i][j-10:j+4]):
                    if selected_data[i][j]==':':   
                        if selected_data[i][j+1]=='、':                      
                            result[i]=selected_data[i][j+2:-1]
                        else: 
                            result[i]=selected_data[i][j+1:-1]
        else: 
            result[i]="N/A"

    for i in range(selected_data.shape[0]):     
        if type(selected_data[i]) is not float:
            for j in range(len(selected_data[i])):
                if "费" in selected_data[i][j+1:j+10]:
                    if selected_data[i][j-1]=='、' :
                        if selected_data[i][j]=='。' :                
                            charge[i]=selected_data[i][j+1:-1]
                        else:                          
                            charge[i]=selected_data[i][j:-1]
        else: 
            charge[i]="N/A"

    for i in range(selected_data.shape[0]):     
        if type(result[i]) is not float:
            for j in range(len(result[i])):
                if result[i][j-1]=='、' :
                    if result[i][j]=='。' :                
                        sentence[i]=result[i][0:j-2]
                    else:                          
                        sentence[i]=result[i][0:j-1]
        else: 
            sentence[i]="N/A"
            
    newdict={
                '判决法条':basis,
                '赔偿结果':charge
                }
    
    #通过字典建立DataFrame，并合并
    newdata=pd.DataFrame(newdict)
    data=pd.concat([data,newdata],axis=1)
    return data

number6(data)
number14(data)
