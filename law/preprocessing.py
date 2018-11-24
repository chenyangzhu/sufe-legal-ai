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
        pass

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
        pass

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
