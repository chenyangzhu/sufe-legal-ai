import numpy as np
import pandas as pd
import jieba
import law.dictionary
import law.utils


# Base Model
class Embedding:
    def __init__(self, dict_dir, jieba_dict):
        '''
        :param:
            dict_dir 是普通的我们构架好的dict，直接用Dicttionary调取
            jieba_dit 是用来输入于jieba里的dict，辅助我们切词，放置在
                        law/dict/jiebadict.txt中
        '''
        self.dictionary = law.dictionary.Dictionary(dict_dir)
        jieba.load_userdict(jieba_dict)
        '''
        For hyper-parameters
        '''

    def cut(self, string, plantiff, defendant, third_party):
        '''
        TODO
        分词 + 全局预处理，将所有包含以下字符的信息，转换为后面的符号
        '地名': PLA
        '原告': PLT
        '被告': DFD
        '第三人': THP
        '标点符号': 直接删除
        '数字': NUMBER
        无法识别的字符/字典里没有的： <UNK>

        :param:
            string str() 需要切词的文件
            plantiff str() 各个被告，用‘、’连接（就是数据库里的那一列）
            defendant str() 各个元告，用'、'连接
            third_party str() 各个第三人，用'、'连接
        '''
        # 以下三个的来源全部都是来自输入的信息
        # Replace 原告名字
        for each_name in plantiff.split('、'):
            string = string.replace(each_name, 'PLT')

        # Replace 被告名字
        for each_name in defendant.split('、'):
            string = string.replace(each_name, 'DFD')

        # Replace 第三人名字
        for each_name in plantiff.split('、'):
            string = string.replace(each_name, 'THP')

        # 以下来源来自我们的字典
        # 直接删除 标点符号
        for each_sign in self.dictionary.sign:
            string = string.replace(each_sign, '')

        # 把涉及到的年月日变为 "DATE"
        string = law.utils.change_date_to_DATE(string)

        # 把涉及到的金钱，全部变为NUMBER，注意了，因为有“万”、“忆”等修饰词，这些词也要弄掉。
        # TOOD 这里可以进一步优化很多
        string = law.utils.change_money_to_MONEY(string)

        cutted = [each_word for each_word in jieba.cut(string)]
        return cutted

    def embed(self, string, plantiff, defendant, third_party):
        '''
        输入一段文字，对这一段文字进行分词+mapping处理
        :param:
            str() 需要输入的string
        :return:
            np.array() 输出的embedding

        Notice that: 这一部分是每一个方法都不同的。
        '''
        # 首先调用cut进行预处理
        cutted = self.cut(string, plantiff, defendant, third_party)
        # 进行一定操作
        embedded = cutted
        return embedded

    def embed_pandas(self, df, targets, plantiff="plantiff",
                     defendant="defendant", third_party="third_party"):
        '''
        这个方程直接输入一个 dataframe, targets 是目标列的名字，可以有多个targets
        '''
        embedded_list = []
        for i in range(df.shape[0]):
            if i % 20 == 0:
                print("Doing", i, ". Total", df.shape[0])
            each_row_embed = []
            for each_target in targets:
                try:
                    each_row_embed.append(self.embed(string=df.iloc[i][each_target],
                                                         plantiff=df.iloc[i][plantiff],
                                                         defendant=df.iloc[i][defendant],
                                                         third_party=df.iloc[i][third_party]))
                except:
                    each_row_embed.append('')
            embedded_list.append(each_row_embed)
        return embedded_list


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
