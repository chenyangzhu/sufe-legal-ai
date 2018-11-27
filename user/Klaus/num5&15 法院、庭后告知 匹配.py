
# coding: utf-8

# In[1]:


import re
import numpy as np
import pandas as pd
import os
import jieba


# State all the possible Hyperparameters you used in this script
file_path = "C:/Users/Klaus/Documents/sufelaw2019/data/crime1.xlsx"
alpha = 10
beta = 10
gamma = 10


# 读取一些数据
data = pd.read_excel(file_path)


# 如果你选择了 5和 15

def number5(data):#法院→省、市、级别，空值采用None填补
    level=[]#法院级别
    distinct=[]#法院所在省
    block=[]#法院所在市区市
    for x in data['法院']:
        #寻找省的字段，如果未找到，使用空值None填补
        a=re.compile(r'.*省')
        b=a.search(x)
        if b==None:
            distinct.append(None)
        else:
            distinct.append(b.group(0))
            x=re.sub(b.group(0),'',x)#删掉省字段，方便寻找市字段

        #找出市的字段，如果未找到，使用空值None填补
        a=re.compile(r'.*市')
        b=a.search(x)
        if b==None:
            block.append(None)
        else:
            block.append(b.group(0))

        #找出级别的字段，如果未找到，使用空值None填补
        a=re.compile(r'.级')
        b=a.search(x)
        if b==None:
            level.append(None)
        else:
            level.append(b.group(0))
    #创建字典，方便创建DataFrame
    newdict={
                '法院所在省':distinct,
                '法院所在市':block,
                '法院等级':level
                }
    #通过字典建立DataFrame，并合并
    newdata=pd.DataFrame(newdict)
    data=pd.concat([data,newdata],axis=1)
    return data

def number15(data):
    final1=[]#是否为终审判决，是为1，不是为0
    final2=[]#是否为终审裁定，是为1，不是为0
    for x in data['庭后告知']:
        if type(x)==type(np.nan):
            final1.append(0)
            final2.append(0)
        else:
            a=re.compile(r'.*为终审判决')
            b=a.search(x)
            if b==None:
                final1.append(0)
            else:
                final1.append(1)

            a=re.compile(r'.*为终审裁定')
            b=a.search(x)
            if b==None:
                final2.append(0)
            else:
                final2.append(1)
    #创建字典，方便创建DataFrame
    newdict={
                '是否为终审判决':final1,
                '是否为终审裁定':final2
                }
    #通过字典建立DataFrame，并合并
    newdata=pd.DataFrame(newdict)
    data=pd.concat([data,newdata],axis=1)
    return data

# 确保所有数据的顺序没有打乱，确保新表的行数没有改变。
# 如果要增加列，全部增加到最后一列。
# 无需删除列。
