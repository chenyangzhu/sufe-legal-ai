import mysql.connector
import pandas as pd
import numpy as np
from mysql.connector.errors import IntegrityError, DataError
import os
import argparse

add_query = ("INSERT INTO Civil "
             # "(title,id,type,proc,class,doc_type,court_name,date,plantiff,defendant,third_party,judge,judge_chief,judge_board,writer,party,procedure,process,opinion,result,notice,appendix)"
             "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='dir help')
parser.add_argument('--u', help="u help")
parser.add_argument('--p', help='p help')
args = parser.parse_args()
direc = args.dir
user = args.u
pwd = args.p

print("Scanning local files..")
file_names = os.listdir(direc)
N = len(file_names)
print(file_names)
print(N,"files detected. Do you wish to upload them all? Press y to proceed, N to cancel. [y/N]")
flag = input()
if flag == "y":
    pass
else:
    exit()

# Connect to mySQL
print("Connecting to server..")
cnx = mysql.connector.connect(user=user, password=pwd,
                              host='cdb-74dx1ytr.gz.tencentcdb.com',port = "10008",
                              database='law')
cursor = cnx.cursor(buffered=True)
print("Server connected!")

for each_name in file_names:
    print("="*30)
    print("Reading",each_name)

    dat = pd.read_excel(direc+"/"+each_name)

    dat = dat[['标题', '案号', '案件类型', '庭审程序', '案由', '文书类型', '法院', '判决日期', '原告', '被告', '第三人', '法官', '审判长', '审判员',
               '书记员', '当事人', '当事人2', '庭审程序说明', '庭审程序说明2', '庭审过程', '庭审过程2', '庭审过程3', '庭审过程4', '庭审过程5',
               '庭审过程6', '法院意见', '法院意见2', '判决结果', '判决结果2', '庭后告知', '庭后告知2', '附录', '附录2']]

    print("Doing Preprocessing.. There are 4 phases...")

    print("[1]Replacing na...")
    dat = dat.replace(np.nan, '', regex=True)

    # 合并重复列到第一列，同时删除重复列

    print("[2]Merging Duplicate Columns")
    dat['当事人'] = dat['当事人'] + dat['当事人2']
    del dat['当事人2']

    dat['庭审程序说明'] = dat['庭审程序说明'] + dat['庭审程序说明2']
    del dat['庭审程序说明2']

    dat['庭审过程'] = dat['庭审过程'] + dat['庭审过程2'] + dat['庭审过程3'] + dat['庭审过程4'] + dat['庭审过程5'] + dat['庭审过程6']
    for i in range(2, 7):
        del dat['庭审过程' + str(i)]

    dat['法院意见'] = dat['法院意见'] + dat['法院意见2']
    del dat['法院意见2']

    dat['判决结果'] = dat['判决结果'] + dat['判决结果2']
    del dat['判决结果2']

    dat['庭后告知'] = dat['庭后告知'] + dat['庭后告知2']
    del dat['庭后告知2']

    dat['附录'] = dat['附录'] + dat['附录2']
    del dat['附录2']

    old_name = list(dat.keys())
    new_name = ["title", "id", "type", "proc", "class", "doc_type", "court_name", "date", "plantiff", "defendant",
                "third_party", "judge", "judge_chief", "judge_board", "writer", "party", "procedure", "process",
                "opinion", "result", "notice", "appendix"]

    print("[3]Changing Column Name to match the server...")
    changing_dict = {}
    assert len(old_name) == len(new_name)
    for i in range(len(old_name)):
        changing_dict[old_name[i]] = new_name[i]

    dat = dat.rename(index=str, columns=changing_dict)

    print("[4]Changing date format to MySQL...")
    date = []
    for each in dat['date']:
        try:
            year = each[:4]
            month = each[5:7]
            day = each[8:10]
            date.append(pd.to_datetime(str(year) + str(month) + str(day)))
        except:
            date.append(pd.to_datetime("20500101"))
    dat['date'] = date

    print("Preprocessing done :]")

    print("Inserting Data into MySQL. This will take up to 1 hr, depending on the data you have.")

    for i in range(len(dat)):
        try:
            cursor.execute(add_query, list(dat.iloc[i]))
        except IntegrityError:
            print("Duplicate Case" + str(dat.iloc[i]['id']) + ". Skipped")
            pass
        except DataError:
            print("Data is wrong in" + str(dat.iloc[i]['id']) + ". Skipped")
            pass
        else:
            print("An unknown error occured." + str(dat.iloc[i]['id']) + "is skipped.")
            pass
        if i % 20 == 0:
            print("doing the " + str(i) + "th data")
            cnx.commit()
            print("Successfully commited to the server.")
