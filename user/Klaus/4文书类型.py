# coding: utf-8

import pandas as pd

# State all the possible Hyperparameters you used in this script

file_path = '/Users/apple/Desktop/123abc.xlsx'


# 并不太懂这个是干嘛的。。。
alpha = 10
beta = 10
gamma = 10


# 读取数据
data = pd.read_excel(file_path)


def number4(data):

    # 将不是裁定书与判决书的文书类型归为其他
    # 其实根据目测文书类型只有这两种，如果不考虑缺失值的话可以把这段删了

    l = len(data)
    for i in range(l):
        if data['文书类型'][i] not in ('裁定书','判决书'):
            data['文书类型'][i] = '其他'


    # 生成 one-hot-code

    data2 = pd.get_dummies(data['文书类型'])
    data3 = pd.concat([data, data2], axis=1)
    data3.rename(columns={'裁定书': '文书类型_是否裁定书','判决书': '文书类型_是否判决书',
                          '其他': '文书类型_是否其他'}, inplace=True)

    return data3  # return a new pandas DataFrame

# 确保所有数据的顺序没有打乱，确保新表的行数没有改变。
# 如果要增加列，全部增加到最后一列。
# 无需删除列。
