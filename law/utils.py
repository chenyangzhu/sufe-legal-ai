import re
import pandas as pd
import numpy as np
import jieba.posseg as pseg
import pymysql


def find_law_in_series(series):
    '''
    Input:
        Pandas Series

    Output:
        Law and its tiao and kuan
        First layer: Iterate through all rows in the Pandas Series
        Second layer: ['law',['tiao','tiao',...],[kuan,kuan,kuan,...]]
    '''

    data_len = len(series)
    findings = []

    for i in range(data_len):
        if pd.isnull(series.iloc[i]):
            findings.append([])
            continue
        try:
            findings.append(find_law_tiao_kuan_in_text(series.iloc[i]))
        except:
            findings.append([])
    return findings


def find_law_tiao_kuan_in_text(string):
    '''
    Given a text containing law, tiao and kuan.
    Sample Input:
    据此，根据《中华人民共和国保险法》第六十五条第二、三款、《中华人民共和国民事诉讼法》
    第六十四条第一款、第一百四十四条规定，判决如下:一、被告中国平安财产保险股份有限公司
    上海分公司、被告中国平安财产保险股份有限公司应于本判决生效之日起十日内支付原告冷桂芝
    保险金人民币888,022.80元；二、原告冷桂芝其他诉讼请求不予支持。、如果未按本判决指定
    的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加
    倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由被
    告平安保险公司、平安保险上海分公司共同负担。

    Sample Output:
    [['《中华人民共和国保险法》', ['第六十五条'], ['第六十五条第二、三款']],
    ['《中华人民共和国民事诉讼法》', ['第六十四条', '第一百四十四条', '第二百五十三条'], ['第六十四条第一款']]]

    Notice:
    保留了款前的条，是因为这样更加方便，更加快捷。
    '''

    final_list = []

    # We first find these "< >"
    sign_find = re.compile(r"《.*?》")

    # We use these names to refind the tiaokuan
    law_list = re.findall(sign_find, string)
    law_set = set(law_list)
    law_length = len(law_set)

    if law_length > 0:  # only do the following when the list is not empty

        # We do this because it's hard to match the law and its tiaokuan.
        for j in range(law_length):
            thislaw = law_set.pop()
            tiao_finder = re.compile(thislaw + r"第.*?条.*?(?:《|。|$)")
            tiao = re.findall(tiao_finder, string)
            # Notice that there might be same laws many times

            real_tiao_list = []
            kuan_list = []

            if len(tiao) > 0:
                for k in range(len(tiao)):
                    if len(tiao[k]) > 0:
                        # Assume that no more than 5 between tiao
                        tiao_finder_plus = re.compile(r"第.{1,5}条")
                        real_tiao = re.findall(tiao_finder_plus, tiao[k])
                        real_tiao_list.extend(real_tiao)

                        for p in range(len(real_tiao)):
                            kuan_finder = re.compile(real_tiao[p] + "第.{1,5}款")
                            kuan = re.findall(kuan_finder, tiao[k])
                            kuan_list.extend(kuan)
            final_list.append([thislaw, real_tiao_list, kuan_list])
    return final_list


def find_something_with_pre(pre, find, string):
    '''
    pre add find - all strings
    '''
    crit = re.compile(pre + ".*?" + find)
    all_result = re.findall(crit, string)
    return all_result[0]


def classify_subject_in_text(text):
    '''
    这个函数，输入一段文字后，判断其中的法人个数、检察院个数等。
    # todo 可以改的更加完善一点；现在的条件还没办法覆盖全部。
    :param text:
    :return:
    '''
    output = [0, 0, 0, 0]  # 自然人 法人 检察院 其他
    if text == np.nan:
        return output

    namelist = text.split('、')
    for name in namelist:
        if not (re.search('公司', name) == None):  # 检查是否为法人
            output[1] += 1
        elif not (re.search('检察院', name) == None):  # 检查是否为检察院
            output[2] += 1
        elif not (re.search('厂', name) == None) and len(name) > 4:  # 检查是否为法人
            output[1] += 1
        elif len(name) <= 4:  # 检查是否为自然人。优化算法时可以把这个提到第一个来检查
            output[0] += 1
        else:
            output[3] += 1  # 检查是否为其他，一般是外国人或名字中不带公司二字的法人
            print(name)
    return output


def getn(string):
    words = pseg.cut(string)
    name = []
    for word, flag in words:
        if flag == 'n':  # 人名词性为nr
            name.append(word)
    return (''.join(name))


def ADBinfo(data, index):
    info = {}
    info['原告'] = []
    info['被告'] = []

    accuser_tag = re.compile(r'原告|上诉人|申请人')
    defender_tag = re.compile(r'被告|被上诉人|被申请人')
    l1 = re.split(defender_tag, data['party'][index])  # 840 844

    proxy = re.compile(r'代理人(.*)')
    legal = re.compile(r'代表人(.*)')
    location = re.compile(r'住所地(.*)|住(.*)|地(.*)|地址(.*)')
    gender = re.compile("男|女")
    date_born = re.compile(r'\d+年\d+月\d+日')
    ethic = re.compile(r'族$')

    a_ind = 0
    d_ind = 0

    for mes in l1:
        mes = re.sub(":", "", mes)
        l2 = re.split("。、", mes)

        # 有一定的结构层次， 但是依然很混乱“、” 分割每个个体的信息 “，”分割个体的属性
        # 有三种关系
        # 原告 被告
        # 上诉人 被上诉人
        # 申请人 被申请人
        # 先把再审信息放在备注

        flag = 0
        a = re.search(accuser_tag, mes)
        if a is not None:  # 1 表示原告信息
            flag = 1
            person = {}
        else:  # 2 表示被告信息
            flag = 2
            person = {}

        for i in range(len(l2)):

            p = re.search(proxy, l2[i])
            le = re.search(legal, l2[i])
            p_gender = re.findall(gender, l2[i])  # 提取性别
            p_birth = re.findall(date_born, l2[i])  # 提取出生日期
            p_location = re.findall(location, l2[i])  # 提取地址

            if len(p_gender) > 0:
                person['性别'] = ''.join(p_gender)
            if len(p_birth) > 0:
                person['出生年月'] = ''.join(p_birth)
            if len(p_location) > 0:
                person['地址'] = ''.join(list(filter(lambda s: s is not '', p_location[0])))

            leth = re.split("，", l2[i])  # 提取民族
            for etho in leth:
                if re.search(ethic, etho) is not None:
                    person['民族'] = ''.join(etho)
            # 委托/诉讼代理人 信息
            if p is not None:
                l4 = re.split("，", l2[i])
                person['委托/诉讼代理人'] = ''.join(re.findall(proxy, l4[0]))
                del (l4[0])
                if len(l4) > 0:
                    person['委托/诉讼代理人公司/职位'] = ''.join(l4)
            # 法定代表人 信息
            if le is not None:
                l4 = re.split("，", l2[i])
                person['法定代表人'] = ''.join(re.findall(legal, l4[0]))
                del (l4[0])
                if len(l4) > 0:
                    person['法定代表人职位'] = getn(''.join(l4))

            if flag is 1:
                person['序号'] = a_ind
                info['原告'].append(person)
                flag = 0
                a_ind = a_ind + 1

            if flag is 2:
                person['序号'] = d_ind
                info['被告'].append(person)
                flag = 0
                d_ind = d_ind + 1

    return (info)


def total_fa_tiao_kuan(data):
    '''
    output:
        借本库find_law_tiao_kuan_in_text函数，以dataframe的形式输出数据库中所有案件所涉及的法、条、款的清单。
    测试：
        尝试运行数据库中的civil表，该表共包含26978条数据(截止至2019年4月7日11:45)，执行时间为0:03:29.822323；
        尝试运行本地数据"侵权.csv"文件，该文件共包含58993条数据，执行时间为0:04:14.327986，尚能尝试改进。
    备注：
        另外本法、条、款清单的查重工作尚需完善。
    '''

    # 连接数据库
    # cnx = pymysql.connect(user='root', password='sufelaw2019',
    #                      host='cdb-74dx1ytr.gz.tencentcdb.com',
    #                      port=10008,
    #                      database='law')

    # 通过pandas阅读数据库内容
    # data = pd.read_sql('SELECT * FROM Civil;', con=cnx)

    # 记录样本数
    sample_n = len(data)

    # 建立空的法、条、款清单
    df_list = pd.DataFrame(columns=['fa', 'tiao', 'kuan'])

    tiao_pattern = re.compile(r'.*条')

    # 填入数据
    for i in range(sample_n):
        if not pd.isnull(data['process'][i]):  # find_law_tiao_kuan_in_text函数不支持nan类型数据输入，故先判断
            try:
                x = find_law_tiao_kuan_in_text(data['process'][i])  # 对于特定的一些字符，find_law_tiao_kuan_in_text会报错
            except:
                print("报错：" + data['id'][i])
            else:
                if len(x) != 0:
                    for element in x:  # 每个element也是一个列表，每个列表中包含一部法的涉及条款
                        if len(element[1]) == 0 and len(element[2]) == 0:  # 即这个列表里只有法，没有条也没有款
                            temp = [element[0], '', '']
                            df_list.loc[df_list.shape[0]] = temp
                        elif len(element[1]) != 0 and len(element[2]) == 0:  # 即这个列表里有法有条但没有款
                            for tiao in element[1]:
                                temp = [element[0], tiao, '']
                                df_list.loc[df_list.shape[0]] = temp
                        elif len(element[1]) != 0 and len(element[2]) != 0:  # 即这个列表有法有条有款
                            existed_tiao_in_kuan = []  # 存储已包含在element[2]中的条
                            for tiao_kuan in element[2]:  # tiao_kuan是一个字符串
                                tiao = tiao_pattern.findall(tiao_kuan)  # 是个list，默认只有一个元素
                                kuan = tiao_kuan.replace(tiao[0], '')
                                existed_tiao_in_kuan.append(tiao[0])
                                temp = [element[0], tiao[0], kuan]
                                df_list.loc[df_list.shape[0]] = temp
    df_list = df_list.drop_duplicates()  # 去重
    df_list = df_list.reset_index(drop = True)  # 重新编排索引,去除原索引
    return df_list


def string2float(string):
    '''
    If the string is convertable to int, return the int.
    If not, return the string back.
    '''
    try:
        return float(string)
    except ValueError:
        return string


def find_word_and_replace(string, find_str, replace_str):
    '''
    TODO
    这个方程在一段文字中，找到一个字符，替换后返回整个字符序列
    :param:
        string:      str()
        find_str:    str()  你要查找的字符
        replace_str: str()  想要替换的字符
    :return:
        string       str()  已经替换后的字符串

    注意：
    1. 如果需要替换的字符不在字符串内，则直接输出
    2. 如果出现两个及以上的字符，必须全部查找。

    算法详情：
    Knuth-Morris-Pratt(KMP)算法 O(n)算法
    https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
    '''

    def kmp_table(W):
        '''
        construct KMP table
        :param:
            W ; the sentence to be analyzied
        :output:
            T ; kmp_table
        '''
        pos = 1
        cnd = 0
        T = [0 for _ in range(len(W)+1)]
        T[0] = -1

        while pos < len(W):
            if W[pos] == W[cnd]:
                T[pos] == T[cnd]
            else:
                T[pos] = cnd
                cnd = T[cnd]
                while cnd >= 0 and W[pos] != W[cnd]:
                    cnd = T[cnd]

            pos += 1
            cnd += 1
        T[pos] = cnd
        return T

        def kmp_search(S, W):
            '''
            input:
                an array of characters, S (the text to be searched)
                an array of characters, W (the word sought)
            output:
                an array of integers, P (positions in S at which W is found)
            '''
            T = kmp_table(S)
            j = 0  # the position of the current character in S
            k = 0  # the position of the current character in W
            P = []  # List to store all the positions that we found in S of W.
            while j < len(S):
                if W[k] == S[j]:
                    j += 1
                    k += 1
                    if k == len(W):
                        P.append(j-k)
                        k = T[k]
                else:
                    k = T[k]
                    if k < 0:
                        j += 1
                        k += 1
            return P

        idx = kmp_search(string, find_str)

        if idx != []:
            output_string = string[:idx[0]-1]

            for i in range(len(idx)-1):
                output_string += replace_str
                output_string += string[idx[i]+len(replace_str):idx[i+1]]

            output_string += string[idx[-1]:]
        else:
            output_string = string

        return output_string


def change_date_to_DATE(string):
    '''
    目标是识别出所有的日期，并且全部改为DATE
    TODO 现在只是一个粗劣版本！
    '''
    b = []
    ct1 = re.compile(r'[0-9]*年')
    ct2 = re.compile(r'[0-9]*月')
    ct3 = re.compile(r'[0-9]*日')
    b.extend(ct1.findall(string))
    b.extend(ct2.findall(string))
    b.extend(ct3.findall(string))

    for each_date in b:
        string = string.replace(each_date, 'DATE')

    return string


def change_money_to_MONEY(string):
    '''
    把所有和钱有关的东西，转换为MONEY
    难点在于可能会出现百元/亿元
    TODO
    '''
    ct1 = re.compile(r'[0-9]*.元')
    b = ct1.findall(string)

    for each_date in b:
        string = string.replace(each_date, 'MONEY')
    return string
