"""
mapping:
'原告':   <PLT>,
'被告':   <DFD>,
'第三人':  <THP>,
'城市':   <CTY>,
'标点符号':<NTT>,
'金钱':   <MNY>
... to be continued
"""

import jieba
import pandas as pd
import numpy as np


def TFIDF(input_data, col_name="process"):
    '''
    input    是我们预处理后的矩阵,是一个pd.DataFrame
    col_name 是我们要做的目标列
    输出词频TFIDF.

    TFIDF的定义和计算方式可以在这里看到 http://www.tfidf.com/
    '''

    cutted = []  # 用来记录切过了的语段
    dic = dict()  # 作为我们的字典，（这里dict的使用方式值得进一步商榷）

    for j in input_data.index:
        # 这是我们在本循环里要处理的一段文字，
        piece = input_data.loc[j]

        # 我们可以采取以下多种方式
        # 方法1：直接用结巴
        cut = [i for i in jieba.cut()]

        # replace是把里面出现的人名等换成特殊字符
        cut = replace(cut, piece)

        for word in cut:
            try:
                dic[word] += 1  # 如果字典里有这个字则加一
            except KeyError:
                dic[word] = 1  # 如果没有则创建这个字于字典中
        cutted.append(cut)

    dictionary = pd.DataFrame.from_dict(dic, orient='index')
    TFidf = dictionary / np.sum(dictionary) * np.log(np.sum(dictionary) / dictionary)
    # 警告！TODO
    # 这里算得TFIDF是你输入进来所有文档的统一的TFIDF，要改成仅对这一行的TFIDF
    return TFidf


def replace(cut, piece):
    '''
    TODO
    这个函数是为了要把结巴分词当中分出来的人名、地名、金钱、年份用特殊字符来代替。

    输入：
    cut：已经经过结巴分词后的一段语句
    piece: 是这一段语句，在预处理后的数据集中所在行

    输出：
    cut：重新整理过的cut
    '''

    return cut
