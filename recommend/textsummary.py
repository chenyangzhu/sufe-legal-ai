#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql
db = pymysql.connect(
     host="cdb-74dx1ytr.gz.tencentcdb.com",# 主机名
     user="root",         # 用户名
     passwd="sufelaw2019",  # 密码
     port=10008,
     db = 'product_dispute')        # 数据库名称


# In[2]:


import pandas as pd
food = pd.read_sql("""SELECT id, process, result FROM product_dispute.case inner join product_dispute.index on product_dispute.case.cnid = product_dispute.index.cnid where process like '%食品%'""",db)


# In[5]:


cursor = db.cursor()
#sql = "INSERT INTO `tab1` (`city`, `region`,`name`) VALUES ('shanghai', 'changnin','xinjinbeiyuan')"
cursor.execute("Drop table summary_case")
cursor.execute("Create table summary_case (                caseid CHAR(20) NOT NULL,                summary LONGTEXT,                ask LONGTEXT,                results LONGTEXT, Primary key(caseid))")
# 
# 


# In[6]:


cursor = db.cursor()
cursor.execute("Show tables")
cursor.fetchall()


# In[7]:


import re 
import numpy as np 

import sys

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def get_ask_and_discription(processdata, i):
    '''
    to parsing the specific case
    processdata: selected case
    i: index
    '''
    #processdata.str.replace('1、.*(。、).*2、')
    if(re.search(re.compile(r'原审判决认定|原审查明|原审法院查明|二审'),processdata['process'][i])):
        return('Not available')
    
    splitcase = processdata['process'].str.split('。、')
    #print(splitcase[i])  
    pos = np.where(pd.Series(splitcase[i]).str.contains('审理终结'))[0]
    #print(len(pos))
    if(len(pos)):
        start = pos[0] + 1#np.min(start_cand[start_cand>pos])
    else:
        start = 0
#start_cand = np.where(pd.Series(splitcase[i]).str.contains('^原告'))[0]
    
#print(start)
    try:
        end_cand = np.where(pd.Series(splitcase[i]).str.contains('辩称'))[0]
        #print(end_cand)
        evi = np.where(pd.Series(splitcase[i]).str.contains('证据如下:'))[0]
        end = np.min(end_cand[end_cand>start])
        if(len(evi)):
            end = np.min(evi, end)

        #证据
        #print(end)
        
    except ValueError:
        end = len(splitcase[i])
        
    filtercase = np.array(splitcase[i][start:end])
   
    try:
        askstring = '诉讼请求|起诉要求:|请求判令:|上诉请求:|要求判令被告方:|诉讼之请:|要求判令|现请求|判令'
        ask0 = []
        askstart = np.where(pd.Series(filtercase).str.contains(askstring))[0][0]
        ask0.append(askstart) 


        if((askstart+1)<end-start):
            if(re.search('2.|2、',filtercase[(askstart+1)])):
                ask0.append(askstart+1)
        if((askstart+2)< end-start):
            if(re.search('3.|3、',filtercase[(askstart+1)])):
                ask0.append(askstart+2)
        
        
        ask = np.array(ask0)
       # print(filtercase[:0])
        output = np.hstack([filtercase[:np.min(ask)],filtercase[(np.max(ask)+1):]])
        
        ##cleaning ask
        askoutput = ';'.join(filtercase[ask])
       
        #print(askoutput)
        #askoutput = re.findall(re.compile(r'请求(.*)'), askoutput)
        reason0 = re.findall(re.compile(r'事实与理由(.*)|事实和理由:(.*)'),'。、'.join(output))
        if reason0:
            reason = reason0[0]
        askoutput = re.sub(re.compile(r'事实与理由(.*)|事实和理由:(.*)'),"",askoutput)
        askoutput = re.sub(re.compile(r'证据:(.*)'),"",askoutput)
        
        
        if len('。、'.join(output))<80:
            summary = '。、'.join(output)
        elif reason0:
            if len(reason) < 80:
                reason = '。、'.join(reason)
                summary = re.sub(re.compile(r'。、|^1|^2|^3|^二|^一|^、[0-9]、||^[0-9]、|^、'),"",reason)
        else:
            tr4s = TextRank4Sentence()
            tr4s.analyze(text='。、'.join(output), lower=True, source = 'all_filters')
            for item in tr4s.get_key_sentences(num = 1):
                summary = item.sentence
                summary = re.sub(re.compile(r'^1|^2|^3|^二|^一|^、[0-9]、|^[0-9]、|^、一、|^、'),"",summary)
        
    except IndexError:
        ask = None
        askoutput = "ask not found"
        if len('。、'.join(filtercase)) < 80:
            summary = '。、'.join(filtercase)
        else:
            tr4s = TextRank4Sentence()
            tr4s.analyze(text='。、'.join(filtercase), lower=True, source = 'all_filters')
            for item in tr4s.get_key_sentences(num=1):
                summary = item.sentence
                summary = re.sub(re.compile(r'^、[0-9]、|^[0-9]、|^、一、|^、'),"",summary)
    
    resultoutput = re.findall(re.compile(r'判决如下:(.*)'), processdata['result'][i])
    result = ';'.join(resultoutput)
    
    caseid = processdata['id'][i]
#     print("id:",caseid)
#     print("summary:",summary) 
#     print()    
#     print("ask:", askoutput)
#     print()    
#     print("result:",';'.join(resultoutput))
   # df={'id':processdata['id'][i],'ask':askoutput, 'summary':summary,'result:':result}
    insert_sql =  "INSERT INTO summary_case (caseid, summary,ask,results) VALUES ('%s','%s','%s','%s' )" % (caseid,summary,askoutput,result) 
    #% (processdata['id'][i],summary,askoutput,result) #INSERT INTO mytable ( age, name ) VALUES ( %s, %s )
 
    cursor.execute(insert_sql) ##执行SQL,绑定dict对应的参数 
    

    


# In[8]:


from tqdm import tqdm
for i in tqdm(range(food.shape[0])):
    try:
        get_ask_and_discription(food,i)
    except:
        print(str(i)+"has some problem")
    


# In[9]:


#get_ask_and_discription(food,1466)
db.commit()
cursor.close()
# 关闭连接
#db.close()    


# In[10]:


pd.read_sql('''select count(*) from summary_case''',db)


# In[ ]:




