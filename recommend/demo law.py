#!/usr/bin/env python
# coding: utf-8
import pymysql
import numpy as np
import pandas as pd 

def recommendlaw(intention,dbcon,number):
    """
    intention: np.array 意图 
    dbcon: database connection
    number: number of recommended laws
    """
    
    lawset = pd.DataFrame(columns= ('article','num'))
    for i in range(intention.shape[0]):
        #关键词匹配
        sql1 = """SELECT article,1 as num FROM cn_company WHERE article like '%""" + intention[i] + """%'""" 
        #append dataframe
        lawset = lawset.append(pd.read_sql_query(sql1,db),ignore_index=True)
    query = pd.DataFrame(lawset)
    #按照匹配意图数量排序
    recommend = query.groupby('article').sum().sort_values('num',ascending = False)
    return(recommend[:number])

if __name__ == 'main':
    intention = np.array(["合同","生产","劳动","仲裁"])
    db = pymysql.connect(
         host="cdb-74dx1ytr.gz.tencentcdb.com",# 主机名
         user="root",         # 用户名
         passwd="sufelaw2019",  # 密码
         port=10008,
         db = 'cn_law')        # 数据库名称
    
   recommendlaw(intention,db,3)




