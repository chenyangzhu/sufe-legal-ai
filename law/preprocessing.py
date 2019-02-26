import pandas as pd
import numpy as np
import re
from law.utils import *
import law.utils
import jieba
import sklearn
import jieba.posseg as pseg


class read_law:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(self.file_path)
        print("Read Data Successful...")
        self.data_len = len(self.data)
        print("This dataset has ", self.data_len, "rows of data.")

        # 处理缺失值，全部用np.nan代替
        self.data = self.data.fillna(np.nan)

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
            if "刑罚变更" in self.data['庭审程序'][i]:
                xingfabiangeng[i] += 1
            if "一审" in self.data['庭审程序'][i]:
                yishen[i] += 1
            if "二审" in self.data['庭审程序'][i]:
                ershen[i] += 1
            if "复核" in self.data['庭审程序'][i]:
                fushen[i] += 1
            if "其他" in self.data['庭审程序'][i]:
                qita[i] += 1

        self.data['庭审程序_是否_刑罚变更'] = xingfabiangeng
        self.data['庭审程序_是否_一审'] = yishen
        self.data['庭审程序_是否_二审'] = ershen
        self.data['庭审程序_是否_复核'] = fushen
        self.data['庭审程序_是否_其他'] = qita
        print(xingfabiangeng)
        print(yishen)
        print(ershen)
        print(qita)

        del xingfabiangeng, yishen, ershen, fushen, qita  # 控制内存

    def number3(self):
        pass

    def number4(self):
        '''
        This function change '文书类型' into one hot encodings
        '''
        panjueshu = np.zeros(self.data_len)
        caidingshu = np.zeros(self.data_len)

        for i in range(self.data_len):
            if "判决书" in self.data['文书类型'][i]:
                panjueshu[i] += 1
            if "裁定书" in self.data['文书类型'][i]:
                caidingshu[i] += 1

        self.data['文书类型_是否_判决书'] = panjueshu
        self.data['文书类型_是否_裁定书'] = caidingshu

        del panjueshu, caidingshu  # 控制内存

    def number5(self):
        '''
            法院→省、市、级别，空值采用None填补
            -- Xu Xiaojie
        '''

        level = []  # 法院级别
        distinct = []  # 法院所在省
        block = []  # 法院所在市区市

        for x in self.data['法院']:
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

        for x in self.data['判决日期']:
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

    def number7(self):
        pass

    def number8(self):
        # http://www.sohu.com/a/249531167_656612
        company = re.compile(r'.*?公司')
        natural_person = np.zeros(self.data_len)
        legal_person = np.zeros(self.data_len)
        other_person = np.zeros(self.data_len)
        for i in range(self.data_len):
            # 显示进度
            if i % 100 == 0:
                print(i)
            # 判断是否缺失
            if pd.isna(self.data['被告'][i]):
                continue
            # 判断是否有字符串中是否有公司
            if re.search(company, self.data['被告'][i]) is not None:
                legal_person[i] = 1
            # 查找名字：按标点分割后长度小于等于4，不含有公司（不考虑外国人和少数民族）
            l = re.split('、', self.data['被告'][i])
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
                    verbs = []
                    for word, flag in words:
                        if flag == 'v':  # 人名词性为nr
                            other_person[i] = 0
                            break

        self.data['被告_是否_自然人'] = natural_person
        self.data['被告_是否_法人'] = legal_person
        self.data['被告_是否_其他'] = other_person

        del natural_person, legal_person, other_person  # 控制内存

    def number9(self):
        pass

    def number10(data):
        data_len = len(data)
        information = []
        for i in range(data_len):
            # 显示进度
            if i % 100 == 0:
                print(i)
            info = {}
             #判断是否缺失 很重要
            if pd.isna(data['当事人'][i]):
               information.append(info)
               information.append({}) #空集合
               continue

            information.append(ADBinfo(data, i))
        self.data['number10'] = information

        del information, info  # 控制内存

    def number11(self):
        pass

    def number12(self):
        pass

    def number13(self):
        pass

    def number14(self):
        '''
        #TODO 这一段有bug，result的那一部分，没有考虑到文本里没有“下”的情况。
        :return:
        '''
        selected_data = self.data["判决结果"]
        result = []  # 判决结果
        basis = []  # 判决依据的条款

        # law packages下载不成功，我就把函数写在这里了
        for i in range(self.data_len):
            if pd.isnull(selected_data.iloc[i]):
                basis.append([])
                continue
            basis.append(law.utils.find_law_tiao_kuan_in_text(selected_data.iloc[i]))

        # 改正这里
        # 查找判决结果，通过“下：、”三层条件进行筛选，空缺殖用N/A进行填补
        for i in range(self.data_len):
            if type(selected_data[i]) is not type(np.nan):
                for j in range(len(selected_data[i])):
                    if selected_data[i][j] == '下':
                        if selected_data[i][j + 1] == ':':
                            if selected_data[i][j + 2] == '、':
                                result.append(selected_data[i][j + 3:-1])
                            else:
                                result.append(selected_data[i][j + 2:-1])
                    # 没有考虑到里面没有“下”的情况。
            else:
                result.append(np.nan)

        print(len(basis),len(result))

        newdict = {
            '判决法条': basis,
            '判决结果': result
        }

        # 通过字典建立DataFrame，并合并
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)

        del selected_data, result, basis, newdict, newdata

    def number15(self):
        '''
        庭后告知 -- Xu Xiaojie
        '''

        final1 = []  # 是否为终审判决，是为1，不是为0
        final2 = []  # 是否为终审裁定，是为1，不是为0

        for x in self.data['庭后告知']:
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
        print(len(final1))
        print(len(final2))
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
        # self.number14()
        # print("#14 finished")
        self.number15()
        print("#15 finished")
        self.number16()
        print("#16 finished")

    def store(self, new_path):
        self.data.to_csv(new_path)


if __name__ == "__main__":
    test = read_law("/home/klaus/Documents/Project/sufelaw2019/data/Finance01.xlsx")
    test.preprocess()
    print(test.data)
    test.store("/home/klaus/Documents/Project/sufelaw2019/data/preFinance01.csv")
