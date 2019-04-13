import numpy as np
import pandas as pd
import jieba


# Base Model
class Embedding:
    def __init__(self, dict_dir):
        self.dictionary = pd.read_xlsx(dict_dir)
        '''
        For hyper-parameters
        '''

    def cut(self, string):
        '''
        TODO
        分词 + 全局预处理，将所有包含以下字符的信息，转换为后面的符号
        '地名': <PLA>;
        '原告': <PLT>,
        '被告': <DFD>,
        '第三人': <THP>,
        '标点符号': <NTT>,
        '数字': TODO  目前不处理数字
        无法识别的字符/字典里没有的： <UNK>
        '''

        cutted = [each_word for each_word in jieba.cut(string)]
        return cutted

    def embed(self, string):
        '''
        输入一段文字，对这一段文字进行分词+mapping处理
        :param:
            str() 需要输入的string
        :return:
            np.array() 输出的embedding
        '''
        cutted = self.cut(string)  # 首先进行预处理
        # 进行一定操作
        return cutted

    def embed_series(self, series):
        '''
        输入是一个pandas的series，或者使用apply function /
        '''
        if type(series) == pd.Series:
            return series.apply(self.embed)
        elif type(series) == pd.DataFrame:
            return series.apply(self.embed, axis=1, result_type="reduce")


class word_freq(Embedding):
    def __init___(self, dict_dir):
        '''
        TODO
        最简单的词频法，用我们已经得到的字典，将字符串分词后对应字典里的词，如果没有这个词，
        则标记为<UNK>

        这个模型的输出是一个 数组 用来表示这段话。
        '''
        super().__init__(dict_dir)

    def embed(self, string):
        string = self.prep(string)
        # TODO Some codes here.
        one_hot = []

        return one_hot


class char_freq(Embedding):
    def __init__(self, dict_dir):
        '''
        TODO
        不使用词频进行统计，完全按照一个一个汉字来处理。
        '''
        pass


class TFIDF(Embedding):
    def __init__(self, dict_dir):
        '''
        TODO
        TFIDF的定义和计算方式可以在这里看到 http://www.tfidf.com/
        '''
        pass


class BERT(Embedding):
    def __init__(self, dict_dir):
        '''
        TODO
        BERT - Bidirectional Encoder Representations from Transformers
        https://arxiv.org/pdf/1810.04805.pdf

        简单介绍这个方法：
        - common words in the model
        - other words are built from character

        例子：
        - “法官”在字典里，返回法官在字典里的序号，
        - “黑人问好”不在字典里，返回[“黑”,“人”，“问”，“号”]，或者返回['黑人','问号']
        '''
        pass
