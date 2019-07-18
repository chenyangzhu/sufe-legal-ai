#!/usr/bin/env python
# coding: utf-8


import pymysql
import pandas as pd 
import re
import numpy as np
def recommendcase(intention,dbcon,number):
    """
    intention: np.array 意图 
    dbcon: database connection
    number: number of recommended laws
    """

    caseset = pd.DataFrame(columns= ('process','result','num'))
    for i in range(intention.shape[0]):
        #关键词匹配
        sql1 = """SELECT process, result,1 as num FROM producer WHERE process like '%""" + intention[i] + """%'""" 
        #append dataframe
        caseset = caseset.append(pd.read_sql_query(sql1,db),ignore_index=True)
    query = pd.DataFrame(caseset)
    #按照匹配意图数量排序
    recommend = query.groupby('process').sum().sort_values('num',ascending = False)
    recommend['process'] = recommend.index
    return(recommend.iloc[:number,])

def get_ask_and_discription(processdata, i=0):
    '''
    to parsing the specific case
    processdata: selected case
    i: index
    '''
    #processdata.str.replace('1、.*(。、).*2、')
    if(re.search(re.compile(r'原审判决认定|原审查明|原审法院查明'),processdata['process'][i])):
        return('Not available')
    
    splitcase = processdata['process'].str.split('。、')
   # print(splitcase[i])  
    pos = np.where(pd.Series(splitcase[i]).str.contains('审理终结'))[0]
    if(~len(pos)):
        start = 0
    else:
        start = pos[0] + 1#np.min(start_cand[start_cand>pos])
#start_cand = np.where(pd.Series(splitcase[i]).str.contains('^原告'))[0]
    
#print(start)
    end_cand = np.where(pd.Series(splitcase[i]).str.contains('^被告|辩称'))[0]
    evi = np.where(pd.Series(splitcase[i]).str.contains('证据如下:'))[0]
    end = np.min(end_cand[end_cand>start])
    if(len(evi)):
        end = np.min(evi, end)

    
    #证据
    #print(end)
    filtercase = np.array(splitcase[i][start:end])
   
    try:
        askstring = '诉讼请求|起诉要求:|请求判令:|上诉请求:|要求判令被告方:|诉讼之请:|要求判令|现请求'
        ask = []
        askstart = np.where(pd.Series(filtercase).str.contains(askstring))[0][0]
        ask.append(askstart) 

        if((askstart+1)<end-start):
            if(re.search('2.|2、',filtercase[(askstart+1)])):
                ask.append(askstart+1)
        if((askstart+2)< end-start):
            if(re.search('3.|3、',filtercase[(askstart+1)])):
                ask.append(askstart+2)

        ask = np.array(ask)
        output = np.hstack([filtercase[:np.min(ask)],filtercase[(np.max(ask)+1):]])
        
        ##cleaning ask
        askoutput = ';'.join(filtercase[ask])
        askoutput = re.findall(re.compile(r'请求(.*)'), askoutput)
        print("ask:", ';'.join(askoutput))
        print("output:",'。、'.join(output))
        
    except IndexError:
        ask = None
        print("ask not found")
        print("output:",'。、'.join(filtercase))
        
    resultoutput = re.findall(re.compile(r'判决如下:(.*)'), processdata['result'][i])
    print("result:",';'.join(resultoutput))
        
      #判决结果&金额
    

if __name__ == 'main':
    
    db = pymysql.connect(
     host="cdb-74dx1ytr.gz.tencentcdb.com",# 主机名
     user="root",         # 用户名
     passwd="sufelaw2019",  # 密码
     port=10008,
     db = 'case')        # 数据库名称

    rec = recommendcase(np.array(['过期','赔偿']),db,1)
    get_ask_and_discription(rec,0)





