import pandas as pd
import numpy as np
import re
from law.utils import *
import jieba.posseg as pseg
import datetime
import mysql.connector


class case_reader:
    def __init__(self, user, password, n=1000, preprocessing=False):
        '''
        n 就是一共需要读取多少种类型，
        preprocessing 是是否需要自动preprocess
        '''
        # 老版本用file_path调用
        # self.file_path = file_path
        # self.data = pd.read_csv(self.file_path, encoding='utf-8', engine='python')
        # 修改读取方式，因为本次使用csv文件读取，所以改成左述形式
        # 新版本，直接传入数据
        # 连接数据库
        self.n = n
        self.preprocessing = preprocessing

        print("Connecting to Server...")
        cnx = mysql.connector.connect(user=user, password=password,
                                      host="cdb-74dx1ytr.gz.tencentcdb.com",
                                      port=10008,
                                      database='law')
        cursor = cnx.cursor(buffered=True)
        print("Server Connected.")

        # 通过pandas阅读数据库内容
        if n>=0:
            query = 'SELECT * FROM Civil LIMIT ' + str(self.n) + ';'
        else:
            query = 'SELECT * FROM Civil;'

        print("Start Reading Data...")
        self.data = pd.read_sql(query,con=cnx)

        print("Read Data Successful...")
        self.data_len = len(self.data)
        print("This dataset has ", self.data_len, "rows of data.")

        # 处理缺失值，全部用np.nan代替
        self.data = self.data.fillna(np.nan)

    def return_data(self):
        if self.preprocessing:
            self.preprocess()
        return self.data

    def number2(self):
        '''
        This function change '庭审程序' into one hot encodings
        -- Klaus
        '''
        xingfabiangeng = np.zeros(self.data_len)
        yishen = np.zeros(self.data_len)
        ershen = np.zeros(self.data_len)
        fushen = np.zeros(self.data_len)
        qita = np.zeros(self.data_len)

        for i in range(self.data_len):
            if self.data['proc'][i] == "刑罚变更":
                xingfabiangeng[i] += 1
            if self.data['proc'][i] == "一审":
                yishen[i] += 1
            if self.data['proc'][i] == "二审":
                ershen[i] += 1
            if self.data['proc'][i] == "复核":
                fushen[i] += 1
            if self.data['proc'][i] == "其他" :
                qita[i] += 1

        self.data['proc_是否_刑罚变更'] = xingfabiangeng
        self.data['proc_是否_一审'] = yishen
        self.data['proc_是否_二审'] = ershen
        self.data['proc_是否_复核'] = fushen
        self.data['proc_是否_其他'] = qita
        #print(xingfabiangeng)
        #print(yishen)
        #print(ershen)
        #print(qita)

        del xingfabiangeng, yishen, ershen, fushen, qita  # 控制内存

    def number3(self):
        '''
        This function change '案由' into one hot encodings
        '''
        reasons = ['机动车交通事故责任纠纷' ,'物件损害责任纠纷' ,'侵权责任纠纷', '产品责任纠纷', '提供劳务者受害责任纠纷' ,'医疗损害责任纠纷',
        '地面施工、地下设施损害责任纠纷', '饲养动物损害责任纠纷' ,'产品销售者责任纠纷', '因申请诉中财产保全损害责任纠纷', '教育机构责任纠纷',
        '违反安全保障义务责任纠纷' , '网络侵权责任纠纷' ,'因申请诉前财产保全损害责任纠纷' ,'物件脱落、坠落损害责任纠纷',
        '因申请诉中证据保全损害责任纠纷' ,'建筑物、构筑物倒塌损害责任纠纷' ,'提供劳务者致害责任纠纷' ,'产品生产者责任纠纷',
        '公共场所管理人责任纠纷', '公证损害责任纠纷', '用人单位责任纠纷' ,'触电人身损害责任纠纷', '义务帮工人受害责任纠纷',
        '高度危险活动损害责任纠纷', '噪声污染责任纠纷' ,'堆放物倒塌致害责任纠纷', '公共道路妨碍通行损害责任纠纷' ,'见义勇为人受害责任纠纷',
        '医疗产品责任纠纷' ,'监护人责任纠纷', '水上运输人身损害责任纠纷', '环境污染责任纠纷', '因申请先予执行损害责任纠纷',
        '铁路运输人身损害责任纠纷' ,'水污染责任纠纷', '林木折断损害责任纠纷', '侵害患者知情同意权责任纠纷' ,'群众性活动组织者责任纠纷',
        '土壤污染责任纠纷']
        mreason = np.zeros(self.data_len)
        for i in range(self.data_len):
            for j,reason in enumerate(reasons):
                if self.data['class'][i] == reasons[j]:
                    mreason[i] +=j+1
        self.data['class_index'] = mreason

        del mreason  # 控制内存

    def number4(self):
        '''
        This function change '文书类型' into one hot encodings
        '''
        panjueshu = np.zeros(self.data_len)
        caidingshu = np.zeros(self.data_len)

        for i in range(self.data_len):
            if self.data['doc_type'][i] == "判决书":
                panjueshu[i] += 1
            if self.data['doc_type'][i] == "裁定书":
                caidingshu[i] += 1

        self.data['doc_type'] = panjueshu
        self.data['doc_type'] = caidingshu

        del panjueshu, caidingshu  # 控制内存

    def number5(self):
        '''
            法院→省、市、级别，空值采用None填补
            -- Xu Xiaojie
        '''

        level = []  # 法院级别
        distinct = []  # 法院所在省
        block = []  # 法院所在市区市

        for x in self.data['court_name']:
            if pd.isna(x):#如果为空
                level.append(None)
                distinct.append(None)
                block.append(None)
            else:#如果不空
                # 寻找省的字段，如果未找到，使用空值None填补
                a = re.compile(r'.*省')
                b = a.search(x)
                if b == None:
                    distinct.append(None)
                else:
                    distinct.append(b.group(0))
                    x = re.sub(b.group(0), '', x)  # 删掉省字段，方便寻找市字段

                # 找出市的字段，如果未找到，使用空值None填补
                a = re.compile(r'.*市')
                b = a.search(x)
                if b == None:
                    block.append(None)
                else:
                    block.append(b.group(0))

                # 找出级别的字段，如果未找到，使用空值None填补
                a = re.compile(r'.级')
                b = a.search(x)
                if b == None:
                    level.append(None)
                else:
                    level.append(b.group(0))

        # 创建字典，方便创建DataFrame
        newdict = {
            '法院所在省': distinct,
            '法院所在市': block,
            '法院等级': level
        }
        # 通过字典建立DataFrame，并合并
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)

        del newdata, level, distinct, block

    def number6(self):
        '''
        分成年月日
        :return:
        '''
        year = []  # 判决年份
        month = []  # 判决月份
        day = []  # 判决日期

        for x in self.data['date']:
            # 寻找年的字段，如果未找到，使用空值None填补
            a = re.compile(r'.*年')
            b = a.search(str(x))
            if b == None:
                year.append(None)
            else:
                year.append(b.group(0))
                x = re.sub(b.group(0), '', x)  # 删掉省字段，方便寻找月字段

            # 找出月的字段，如果未找到，使用空值None填补
            a1 = re.compile(r'.*月')
            b1 = a1.search(str(x))
            if b1 == None:
                month.append(None)
            else:
                month.append(b1.group(0))
                x = re.sub(b1.group(0), '', x)  # 删掉省字段，方便寻找日字段

            # 找出日的字段，如果未找到，使用空值None填补
            a2 = re.compile(r'.*日')
            b2 = a2.search(str(x))
            if b2 == None:
                day.append(None)
            else:
                day.append(b2.group(0))

        # 创建字典，方便创建DataFrame
        newdict = {
            '判决年份': year,
            '判决月份': month,
            '判决日期': day
        }
        # 通过字典建立DataFrame，并合并
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)

        del year, month, day

    def number7(self):  # 四列 one hot 检察院，法人，自然人，其他
        '''根据属性“原告”判断有无检察院，法人，自然人，其他（有：1；无：0）
        ***概念分析：检查院也属于法人，所以如果检察院为1，那么法人也为1。
        基于假设：
        -检察院的名字最后含有“检察院”三个字，则可以根据属性“原告”切词后是否有“检察院”字样的子集进行判断
        -自然人的名字不超过四个字，则可以根据属性“原告”切词后是否有少于四字的子集进行判断
        -法人：如果有检察院；则自然有法人；如果含有“公司”字样，同样可以判定有法人
        -其他：如果切词所得的结果不满足上述三个任意条件，则属于其他
        --Xu Xiaojie
        '''

        # 初始化新列
        self.data['原告_是否_检察院'] = 0
        self.data['原告_是否_法人'] = 0
        self.data['原告_是否_自然人'] = 0
        self.data['原告_是否_其他'] = 0

        # 开始处理
        pattern = r'(?::|：|。|、|\s|，|,)\s*'  # 分词符号匹配，包括中英文冒号，句号，顿号，空格等
        jcy_pattern = re.compile(r'.*检察院')  # 编译检察院的关键字匹配
        gs_pattern = re.compile(r'.*公司')  # 编译公司的关键字匹配
        for i in range(len(self.data['plantiff'])):
            # 如果是空值，直接跳过
            if pd.isna(self.data['plantiff'][i]):
                continue
            # 如果非空，那么开始分词
            self.data['plantiff'][i] = re.sub(' ', '', self.data['plantiff'][i])  # 先把每行数据的空格去掉
            result_list = re.split(pattern, self.data['plantiff'][i])  # 分词后得到的是一个列表
            for x in result_list:
                temp1 = jcy_pattern.findall(x)  # temp1返回的是list，里面的元素为包含'检察院'字样的元素
                temp2 = gs_pattern.findall(x)  # temp2返回的是list，里面的元素为包含'公司'字样的元素
                # 判断是否有检察院
                if len(temp1) != 0:  # list非空，说明有检察院
                    self.data['原告_是否_检察院'][i] = 1
                # 判定是否有自然人
                if (0 < len(x) <= 4):
                    self.data['原告_是否_自然人'][i] = 1
                # 判定是否有法人
                if ((len(temp1) != 0) or len(temp2) != 0):
                    self.data['原告_是否_法人'][i] = 1
                # 判定是否有其他
                if (len(x) > 4 and len(temp1) == 0 and len(temp2) == 0):
                    self.data['原告_是否_其他'][i] = 1

    def number8(self):
        # http://www.sohu.com/a/249531167_656612
        company = re.compile(r'.*?公司')
        natural_person = np.zeros(self.data_len)
        legal_person = np.zeros(self.data_len)
        other_person = np.zeros(self.data_len)
        for i in range(self.data_len):
            # 显示进度
            #if i % 100 == 0:
            #    print(i)
            # 判断是否缺失
            if pd.isna(self.data['defendant'][i]):
                continue
            # 判断是否有字符串中是否有公司
            if re.search(company, self.data['defendant'][i]) is not None:
                legal_person[i] = 1
            # 查找名字：按标点分割后长度小于等于4，不含有公司（不考虑外国人和少数民族）
            l = re.split('、', self.data['defendant'][i])
            l1 = list(filter(lambda s: len(s) <= 4, l))
            l2 = list(filter(lambda s: (re.search(company, s)) is None, l1))
            if len(l2) > 0:
                natural_person[i] = 1
            # 查找其他：按标点分割后长度大于4，不含有公司，且不含有谓语动词（数据有时会将起诉原因一并放入被告栏）
            l3 = list(filter(lambda s: len(s) > 4, l))
            l4 = list(filter(lambda s: (re.search(company, s)) is None, l3))
            if len(l4) > 0:
                other_person[i] = 1
                for mes in l4:
                    words = pseg.cut(mes)
                    #verbs = []
                    for word, flag in words:
                        if flag == 'v':  # 人名词性为nr
                            other_person[i] = 0
                            break

        self.data['被告_是否_自然人'] = natural_person
        self.data['被告_是否_法人'] = legal_person
        self.data['被告_是否_其他'] = other_person

        del natural_person, legal_person, other_person  # 控制内存

    def number9(self):
        '''根据属性“第三人”判断有无自然人（有：1；无：0）
        基于假设：自然人的名字不超过四个字，则可以根据属性“第三人”切词后是否有少于四字的子集进行判断
        --Xu Xiaojie'''

        self.data['第三人_有无自然人'] = 0  # 初始化新的列
        pattern = r'(?::|：|。|、|\s|，|,)\s*'  # 分词符号匹配，包括中英文冒号，句号，顿号，空格等
        for i in range(len(self.data['third_party'])):
            # 如果是空值，直接跳过
            if pd.isna(self.data['third_party'][i]):
                continue
            # 如果非空，那么开始分词
            result_list = re.split(pattern, self.data['third_party'][i])  # 得到的是一个列表
            # 遍历分词列表中的每个元素，如果有长度小于等4大于0的字符串，则说明有自然人
            for x in result_list:
                if (0 < len(x) <= 4):
                    self.data['第三人_有无自然人'][i] = 1
                    break  # 找到了就可以退出了，不需要遍历剩下的列表元素，节省时间

    def number10(self):
        information = []
        for i in range(self.data_len):
            # 显示进度
            #if i % 100 == 0:
                #print(i)
            info = {}
            # 判断是否缺失 很重要
            if pd.isna(self.data['party'][i]):
                information.append({})  # 空集合
                continue

            information.append(ADBinfo(self.data, i))
        self.data['party_one_hot'] = information

        del information, info  # 控制内存

    def number11(self):
        types = []  # 程序类别
        money = []
        for x in self.data['procedure']: # 这里上传的时候要改成self.data['庭审程序说明']
            #print(x)
            if str(x)=='nan' or re.search('[0-9]+元',x)==None:
                money.append(0)
            else:
                money.append(1)
            if str(x)=='nan':
                types.append('空白')
            elif not(re.search('不宜在互联网公布|涉及国家秘密的|未成年人犯罪的',x)==None):
                types.append('不公开')
            elif not(re.search('以调解方式结案的',x)==None):
                types.append('调解结案')
            elif not(re.search('一案.*本院.*简易程序.*(因|转为)',x)==None):
                types.append('已审理（简易转普通）')
            elif not(re.search('一案.*(小额诉讼程序|简易程序).*审理(。$|终结。$|.*到庭参加诉讼|.*到庭应诉|.*参加诉讼)',x)==None):
                types.append('已审理（简易）')
            elif not(re.search('(一案.*本院.*(审理。$|审理终结。$|公开开庭进行了审理。$|公开开庭进行.?审理.*到庭参加.?诉讼))',x)==None):
                types.append('已审理')
            #elif not(re.search('一案.*本院.*(受理|立案).*简易程序.*(因|转为)',x)==None):
                #types.append('已受理/立案（简易转普通）')
                #这种情况出现的太少，暂不单独分类
            elif not(re.search('一案.*本院.*(受理|立案).*(小额诉讼程序|简易程序)(。$|.*由.*审判。$)',x)==None):
                types.append('已受理/立案（简易）')
            elif not(re.search('一案.*本院.*(立案。$|立案受理。$|立案后。$)',x)==None):
                types.append('已受理/立案')
            elif not(re.search('一案.*(调解.*原告|原告.*调解).*撤',x)==None):
                types.append('调解撤诉')
            elif (re.search('调解',x)==None) and not(re.search('一案.*原告.*撤',x)==None):
                types.append('其他撤诉')
            elif not(re.search('一案.*原告.*((未|不).*(受理|诉讼)费|(受理|诉讼)费.*(未|不))',x)==None):
                types.append('未交费')
            elif not(re.search('一案.*本院.*依法追加.*被告',x)==None):
                types.append('追加被告')
            elif not(re.search('上诉人.*不服.*上诉。$',x)==None):
                types.append('上诉')
            elif not(re.search('再审.*一案.*不服.*再审。$',x)==None):
                types.append('要求再审')
            elif not(re.search('一案.*申请财产保全.*符合法律规定。$',x)==None):
                types.append('同意诉前财产保全')
            elif not(re.search('申请.*(请求|要求).*(查封|冻结|扣押|保全措施)',x)==None):
                types.append('申请财产保全')
            elif not(re.search('一案.*(缺席|拒不到庭|未到庭)',x)==None):
                types.append('缺席审判')
            elif not(re.search('一案.*申请.*解除(查封|冻结|扣押|保全措施).*符合法律规定。$',x)==None):
                types.append('同意解除冻结')
            else:
                types.append('其他/错误')

        #newdict={'庭审程序分类':types,'money':money}
        newdict={'庭审程序分类':types}
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)
        del types

    def number12(self):

        #1.是否撤诉
        repeal_pattern = re.compile(r'撤诉')

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)

        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = repeal_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否撤诉_是'] = yes
        self.data['庭审过程_是否撤诉_未知'] = dk
        self.data['庭审过程_是否撤诉_否'] = no
        self.data['庭审过程_是否撤诉_汇总'] = al


        del yes, no, dk, al



        #2.是否受伤
        situation_pattern = re.compile(r'受伤|死亡|伤残|残疾|致残')

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)


        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = situation_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否受伤_是'] = yes
        self.data['庭审过程_是否受伤_否'] = no
        self.data['庭审过程_是否受伤_未知'] = dk
        self.data['庭审过程_是否受伤_汇总'] = al


        del yes, no, dk, al




        #3. 是否涉及金钱
        money_pattern = re.compile(r'[0-9]+元|[0-9]+万元|[0-9]+万+[0-9]+千元|[0-9]+千+[0-9]+百元'
                                   r'[0-9]+万+[0-9]+千+[0-9]+百元|[0-9]+,+[0-9]+元|[0-9]+,+[0-9]+,+[0-9]+元')

        '''
        包含xxx元 xxx万元 xxx万xxx千元 xxx万xxx千xxx百元 xxx千xxx百元 xxx,xxx元 xxx,xxx,xxx元
        '''

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)


        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = money_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否涉及金钱_是'] = yes
        self.data['庭审过程_是否涉及金钱_否'] = no
        self.data['庭审过程_是否涉及金钱_未知'] = dk
        self.data['庭审过程_是否涉及金钱_汇总'] = al


        del yes, no, dk, al



        #4. 是否故意
        intent_pattern = re.compile(r'有意|故意')

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)


        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = intent_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否故意_是'] = yes
        self.data['庭审过程_是否故意_否'] = no
        self.data['庭审过程_是否故意_未知'] = dk
        self.data['庭审过程_是否故意_汇总'] = al


        del yes, no, dk, al




        #5. 是否要求精神赔偿
        mental_pattern = re.compile(r'精神损失|精神赔偿|精神抚慰')

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)


        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = mental_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否要求精神赔偿_是'] = yes
        self.data['庭审过程_是否要求精神赔偿_否'] = no
        self.data['庭审过程_是否要求精神赔偿_未知'] = dk
        self.data['庭审过程_是否要求精神赔偿_汇总'] = al


        del yes, no, dk, al




        #6. 是否拒不出庭
        absent_pattern = re.compile(r'拒不到庭')

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)


        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = absent_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否拒不到庭_是'] = yes
        self.data['庭审过程_是否拒不到庭_否'] = no
        self.data['庭审过程_是否拒不到庭_未知'] = dk
        self.data['庭审过程_是否拒不到庭_汇总'] = al


        del yes, no, dk, al


        #7. 是否有异议、申请重新判决
        objection_pattern = re.compile(r'有异议|重新鉴定|判决异议|')

        yes = np.zeros(self.data_len)
        no = np.zeros(self.data_len)
        dk = np.zeros(self.data_len)
        al = np.zeros(self.data_len)


        for i in range(self.data_len):

            if not pd.isna(self.data['process'][i]):

                temp = objection_pattern.findall(str(self.data['process'][i]))

                if len(temp) == 0:
                    no[i] += 1
                    al[i] = 0

                else:
                    yes[i] += 1
                    al[i] = 1

            else:
                dk[i] += 1
                al[i] = -1

        self.data['庭审过程_是否有异议_是'] = yes
        self.data['庭审过程_是否有异议_否'] = no
        self.data['庭审过程_是否有异议_未知'] = dk
        self.data['庭审过程_是否有异议_汇总'] = al


        del yes, no, dk, al

        #8. 判决书长度
        length = np.zeros(self.data_len)

        for i in range(self.data_len):
            if type(self.data['process'][i]) == str:
                length[i] = len(self.data['process'][i])
            else:
                length[i] = 0

        self.data['庭审过程_长度'] = length

        del length


    def number13(self):
        '''根据属性“法院意见”抓取出如下信息：
        -案件是否涉及赔偿金额
        -案件涉及的法数
        -案件涉及的条数
        -案件涉及的款数
                --Xu Xiaojie'''

        #  初始化新的属性列
        self.data['法院意见_是否涉及金额'] = 0
        self.data['法院意见_涉及的法数'] = 0
        self.data['法院意见_涉及的条数'] = 0
        self.data['法院意见_涉及的款数'] = 0

        money_pattern = re.compile(r'[0-9]+元')  # 是否涉及金额匹配
        #  先处理法、条、款数
        for i in range(len(self.data['opinion'])):
            if not pd.isna(self.data['opinion'][i]):  # 如果非空
                try:
                    temp = find_law_tiao_kuan_in_text(self.data['opinion'][i])#返回的是一个有法、条、款的列表
                except:
                    print('法院意见无法处理的案件案号:'+self.data['id'][i])
                else:
                    if len(temp) > 0:
                        self.data['法院意见_涉及的法数'][i] = len(temp)#法数
                        #条数，款数
                        sum_tiao = 0
                        sum_kuan = 0
                        for j in range(len(temp)):
                            sum_tiao += len(temp[j][1])#加和条数
                            sum_kuan += len(temp[j][2])#加和款数
                        self.data['法院意见_涉及的条数'][i] = sum_tiao
                        self.data['法院意见_涉及的款数'][i] = sum_kuan

        # 再处理金额问题
        for i in range(len(self.data['opinion'])):
            if not pd.isna(self.data['opinion'][i]):  # 如果非空
                temp1 = money_pattern.findall(self.data['opinion'][i])  # temp1返回的是list，里面的元素为包含'XX元'字样的元素
                if len(temp1) == 0:  # 没有‘元’字样直接跳过
                    continue
                self.data['法院意见_是否涉及金额'][i] = 1  # 不满足上述条件，则涉及金额

    def number14(self):
        selected_data = self.data["result"]
        data_len = len(selected_data)

        basis = []  # 判决依据的条款
        result = ["N/A"] * data_len  # 判决结果
        charge = ["N/A"] * data_len
        sentence = ["N/A"] * data_len

        for i in range(data_len):
            if pd.isnull(selected_data.iloc[i]):
                basis.append([])
                continue
            basis.append(find_law_tiao_kuan_in_text(selected_data.iloc[i]))

        #  查找判决结果，空缺值用N/A进行填补
        for i in range(selected_data.shape[0]):
            if type(selected_data[i]) is not float:
                for j in range(len(selected_data[i])):
                    if ("判决" in selected_data[i][j - 4:j + 4] or "裁定" in selected_data[i][j - 4:j + 4]) and (
                            "法院" not in selected_data[i][j - 10:j + 4]):
                        if selected_data[i][j] == ':':
                            if selected_data[i][j + 1] == '、':
                                result[i] = selected_data[i][j + 2:-1]
                            else:
                                result[i] = selected_data[i][j + 1:-1]
            else:
                result[i] = "N/A"

        for i in range(selected_data.shape[0]):
            if type(selected_data[i]) is not float:
                for j in range(len(selected_data[i])):
                    if "费" in selected_data[i][j + 1:j + 10]:
                        if selected_data[i][j - 1] == '、':
                            if selected_data[i][j] == '。':
                                charge[i] = selected_data[i][j + 1:-1]
                            else:
                                charge[i] = selected_data[i][j:-1]
            else:
                charge[i] = "N/A"

        for i in range(selected_data.shape[0]):
            if type(result[i]) is not float:
                for j in range(len(result[i])):
                    if result[i][j - 1] == '、':
                        if result[i][j] == '。':
                            sentence[i] = result[i][0:j - 2]
                        else:
                            sentence[i] = result[i][0:j - 1]
            else:
                sentence[i] = "N/A"

        newdict = {
            '判决法条': basis,
            '赔偿结果': charge
        }

        # 通过字典建立DataFrame，并合并
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)

        del newdata, newdict, basis, result, charge, sentence

    def number15(self):
        '''
        庭后告知 -- Xu Xiaojie
        '''

        final1 = []  # 是否为终审判决，是为1，不是为0
        final2 = []  # 是否为终审裁定，是为1，不是为0

        for x in self.data['notice']:
            if type(x) == type(np.nan):
                final1.append(0)
                final2.append(0)
            else:
                a = re.compile(r'.*为终审判决')
                b = a.search(x)
                if b == None:
                    final1.append(0)
                else:
                    final1.append(1)

                a = re.compile(r'.*为终审裁定')
                b = a.search(x)
                if b == None:
                    final2.append(0)
                else:
                    final2.append(1)
        #print(len(final1))
        #print(len(final2))
        # 创建字典，方便创建DataFrame
        newdict = {
            '是否为终审判决': final1,
            '是否为终审裁定': final2
        }

        # 通过字典建立DataFrame，并合并
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)

        del newdata, final1, final2, newdict

    def number16(self):
        '''
        Appendix
        '''
        pass

    def preprocess(self):
        self.number2()
        print("#2 finished")
        self.number3()
        print("#3 finished")
        self.number4()
        print("#4 finished")
        self.number5()
        print("#5 finished")
        self.number6()
        print("#6 finished")
        self.number7()
        print("#7 finished")
        self.number8()
        print("#8 finished")
        self.number9()
        print("#9 finished")
        self.number10()
        print("#10 finished")
        self.number11()
        print("#11 finished")
        self.number12()
        print("#12 finished")
        self.number13()
        print("#13 finished")
        self.number14()
        print("#14 finished")
        self.number15()
        print("#15 finished")
        self.number16()
        print("#16 finished")

    def store(self):
        self.data.to_csv("./.cache/" + str(datetime.time()))

class law_reader:
    def __init__(self, user, password):

        print("Connecting to Server...")
        self.cnx = mysql.connector.connect(user=user, password=password,
                                      host="cdb-74dx1ytr.gz.tencentcdb.com",
                                      port=10008,
                                      database='law_article')
        self.cursor = self.cnx.cursor(buffered=True)
        print("Server Connected.")

    def return_full_law(self, law_name):
        '''
        返回你指定的法律文献
        :param law_name:        string           必须是英语
        :return:                pd.Dataframe
        '''
        law_name = law_name

        # 通过pandas阅读数据库内容
        query = 'SELECT * FROM ' + law_name + ';'

        print("Start Reading Law...")
        law_article = pd.read_sql(query, con=self.cnx)

        return law_article

    def query(self, law_name:str, tiao:int):

        '''
        :param law_name:  string    法律名称，注意必须是英语
        :param tiao:      int       条款序号，
        :return: law      dict     [index，tag1，tag2，tag3，tag4，tag5，article]
        '''

        assert type(tiao) == int
        query = 'SELECT * FROM ' + law_name + ' WHERE '+law_name+'.index = '+str(tiao)+';'
        print("Start Querying")
        law_article = pd.read_sql(query, con=self.cnx)
        law_article = law_article.iloc[0].to_dict()

        return law_article
