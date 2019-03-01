import re
import pandas as pd
import numpy as np
import jieba.posseg as pseg
import jieba

entity_ac = np.array(('原告', '上诉人', '申请人'))
entity_df = np.array(('被告', '被上诉人', '被申请人'))
entity = np.vstack((entity_ac, entity_df))


### Ultimate function we need is Entity_Extractor()

def StruStr(String):
    pattern = ':|：|。|、，'
    result_list = re.split(pattern, String)
    accuser = []
    defender = []
    for j in range(len(result_list)):
        for i in range(entity.shape[1]):
            if re.search(re.compile("[^!被]" + entity[0, i]), " " + result_list[j]) and len(result_list[j]) <= len(
                    entity[1, i]) + 1:
                accuser.append(result_list[j + 1])
            elif re.search(entity[1, i], result_list[j]) and len(result_list[j]) <= len(entity[0, i]) + 2:
                defender.append(result_list[j + 1])
    return (accuser, defender)


# 非结构化语句
def NatuStr(String):
    pattern = r',|。|，|；'
    result_list = re.split(pattern, String)
    accuser = []
    defender = []
    for j in range(len(result_list)):
        for i in range(entity.shape[1]):
            s0 = re.search(re.compile("[^!被]" + entity[0, i]), " " + result_list[j])
            s1 = re.search(entity[1, i], result_list[j])
            if s0 and s1:
                continue
            elif s0 and len(result_list[j]) >= len(entity[1, i]) + 1:
                accuser.append(re.sub(entity[0, i], "", result_list[j]))
            elif s1 and len(result_list[j]) >= len(entity[0, i]) + 1:
                defender.append(re.sub(entity[1, i], "", result_list[j]))
            ##如果有被上诉人应该忽略被告 因为被告指的是原审
    return (accuser, defender)


def OneStr(String):
    seri = []
    accuser = []
    defender = []

    s0 = re.finditer(entity[0, 0], String)
    s1 = re.finditer(entity[1, 0], String)
    s = [s0, s1]
    for j in range(1, -1, -1):
        if s[j]:
            # j = 0 原告','上诉人','申请人' j = 1 '被告','被上诉人','被申请人'
            for it in s[j]:
                seri.append((j, it.span()))
    # print(seri)

    for i in range(1, entity.shape[1]):
        s0 = re.finditer(re.compile("[^!被]" + entity[0, i]), String)
        s1 = re.finditer(entity[1, i], String)
        s = [s0, s1]
        for j in range(1, -1, -1):
            if s[j]:
                # j = 0 原告','上诉人','申请人' j = 1 '被告','被上诉人','被申请人'
                for it in s[j]:
                    seri.append((j, it.span()))
                    # print(seri)

                    # 获得分割位置
    enumber = np.hstack(seri[i][1] for i in range(len(seri)))
    index = np.sort(enumber)
    order = np.argsort(enumber)
    # print(order)
    # 出于对庭审过程类似的字符串考虑，应该限制抓取长度。 并且认为在同一段文字中 对于原告被告的陈述会在靠前的位置
    # 并且认为重复出现同一主体（公司等表示 陈述结束）
    # 在非结构化的字符串中，一般不会在一个“被告”后加多个主体。。
    i = 0
    accuser = []
    defender = []
    while i <= len(index) - 1:  # 类型
        # print(order[i]/2)
        j = seri[np.int(order[i] / 2)][0]
        if i == len(index) - 2:
            content = String[index[i + 1]:(index[i + 1] + 30)]
        else:
            content = String[index[i + 1]:index[i + 2]]
        if j:
            defender.append(content)
        else:
            accuser.append(content)
        i = i + 2
    return (accuser, defender)

    # stringnew = string1[index[0]:(index[0]+50)]
    # index[np.argwhere(index == 3)+1]


def JudgeE(strlist):
    company = re.compile(r'.*?公司|.*?有限公.*')
    natural_person = 0
    legal_person = 0
    other_person = 0
    if strlist.shape[0]:
        for i in range(strlist.shape[0]):
            # 显示进度
            if i % 10 == 0:
                print(i)
                # 判断是否缺失
            if pd.isna(strlist[i]):
                continue
                # 判断是否有字符串中是否有公司
            if re.search(company, strlist[i]) is not None:
                legal_person = 1
                # 查找名字：按标点分割后长度小于等于4，不含有公司（不考虑外国人和少数民族）
            l = re.split('、', strlist[i])
            l2 = list(filter(lambda s: (re.search(company, s)) is None, l))
            if len(l2) > 0:
                for mes in l2:
                    words0 = pseg.cut(mes)
                    for word, flag in words0:
                        if flag == 'nr':  # 人名词性为nr
                            natural_person = 1
                            break
            if natural_person + legal_person == 0:
                other_person = 1

    return (natural_person, legal_person, other_person)


def Entity_Extractor(String):
    # http://www.sohu.com/a/249531167_656612
    data = {}
    ac_natural_person = 0
    ac_legal_person = 0
    ac_other_person = 0

    df_natural_person = 0
    df_legal_person = 0
    df_other_person = 0

    accuser0, defender0 = StruStr(String)
    accuser1, defender1 = NatuStr(String)
    accuser2, defender2 = OneStr(String)
    accuser = np.hstack((accuser0, accuser1, accuser2))
    defender = np.hstack((defender0, defender1, defender2))
    print("原告", accuser)
    print("被告", defender)

    ac_natural_person, ac_legal_person, ac_other_person = JudgeE(accuser)
    df_natural_person, df_legal_person, df_other_person = JudgeE(defender)

    data['被告_是否_自然人'] = df_natural_person
    data['被告_是否_法人'] = df_legal_person
    data['被告_是否_其他'] = df_other_person

    data['原告_是否_自然人'] = ac_natural_person
    data['原告_是否_法人'] = ac_legal_person
    data['原告_是否_其他'] = ac_other_person

    del ac_natural_person, ac_legal_person, ac_other_person,
    df_natural_person, df_legal_person, df_other_person  # 控制内存

    return data  # return a new pandas DataFrame
