import pandas as pd
import numpy as np
import re
import jieba
import sklearn

class read_law:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(self.file_path)
        print("Read Data Successful...")
        self.data_len = len(self.data)
        print("This dataset has ", self.data_len, "rows of data.")

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

        del xingfabiangeng, yishen, ershen, fushen, qita   # 控制内存

    def number3(self):
        pass

    def number4(self):
        pass

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
                x = re.sub(b.group(0), '', x)#删掉省字段，方便寻找市字段

            #找出市的字段，如果未找到，使用空值None填补
            a = re.compile(r'.*市')
            b = a.search(x)
            if b == None:
                block.append(None)
            else:
                block.append(b.group(0))

            #找出级别的字段，如果未找到，使用空值None填补
            a = re.compile(r'.级')
            b = a.search(x)
            if b == None:
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
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data, newdata], axis=1)

        del newdata, level, distinct, block

    def number6(self):
        pass

    def number7(self):
        pass

    def number8(self):
        pass

    def number9(self):
        '''
        Klaus
        ---
        This function take turns "第三人" into one hot
        '''


    def number10(self):
        pass

    def number11(self):
        pass

    def number12(self):
        pass

    def number13(self):
        pass

    def number14(self):
        pass

    def number15(self):
        '''
        庭后告知 -- Xu Xiaojie
        '''

        final1 = []#是否为终审判决，是为1，不是为0
        final2 = []#是否为终审裁定，是为1，不是为0

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

        #创建字典，方便创建DataFrame
        newdict = {
                    '是否为终审判决':final1,
                    '是否为终审裁定':final2
                    }

        #通过字典建立DataFrame，并合并
        newdata = pd.DataFrame(newdict)
        self.data = pd.concat([self.data,newdata],axis=1)

        del newdata, final1, final2, newdict

    def number16(self):
        pass

    def preprocess(self):
        self.number2()
        self.number3()
        self.number4()
        self.number5()
        self.number6()
        self.number7()
        self.number8()
        self.number9()
        self.number10()
        self.number11()
        self.number12()
        self.number13()
        self.number14()
        self.number15()
        self.number16()

    def store(self, new_path):
        self.data.to_csv(new_path)
