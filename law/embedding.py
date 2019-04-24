import numpy as np
import pandas as pd
import jieba
import law.utils
import law


# Base Model
class Embedding:
    def __init__(self, dict_dir, jieba_dict):
        '''
        :param:
            dict_dir 是普通的我们构架好的dict，直接用Dicttionary调取
            jieba_dit 是用来输入于jieba里的dict，辅助我们切词，放置在
                        law/dict/jiebadict.txt中
        '''
        self.dictionary = law.Dictionary(dict_dir)
        jieba.load_userdict(jieba_dict)
        '''
        For hyper-parameters
        '''

    def transform(self, string, plantiff=None, defendant=None, third_party=None):
        '''
        这一部分，主要做的是 entity identification.

        全局预处理，将所有包含以下字符的信息，转换为后面的符号
        '地名': PLA
        '原告': PLT
        '被告': DFD
        '第三人': THP
        '标点符号': 直接删除
        '数字': NUMBER

        :param:
            string str() 需要切词的文件
            plantiff str() 各个被告，用‘、’连接（就是数据库里的那一列）
            defendant str() 各个元告，用'、'连接
            third_party str() 各个第三人，用'、'连接

        :output:
            transformed string
        '''
        # 以下三个的来源全部都是来自输入的信息
        # Replace 原告名字
        if not plantiff: # Make sure it's not none
            for each_name in plantiff.split('、'):
                string = str(string).replace(each_name, 'PLT')

        # Replace 被告名字
        if not defendant:
            for each_name in defendant.split('、'):
                string = str(string).replace(each_name, 'DFD')

        # Replace 第三人名字
        if not plantiff:
            for each_name in plantiff.split('、'):
                string = str(string).replace(each_name, 'THP')

        # 以下来源来自我们的字典
        # 直接删除 标点符号
        for each_sign in self.dictionary.sign:
            # The extra str is to make sure that replace would work
            string = str(string).replace(each_sign, '')

        # 把涉及到的年月日变为 "DATE"
        # TODO, 这里的方法让date没办法用结巴分词分开
        string = law.utils.change_date_to_DATE(string)

        # 把涉及到的金钱，全部变为NUMBER，注意了，因为有“万”、“忆”等修饰词，这些词也要弄掉。
        # TOOD 这里可以进一步优化很多
        string = law.utils.change_money_to_MONEY(string)

        return string

    def cut(self, transformed):
        '''
        目前使用结巴分词分词，之后可以更改
        character-level model 不需要分词
        TODO 可能需要手动把大写英语字母切开
        '''
        cutted = [each_word for each_word in jieba.cut(transformed)]
        return cutted

    def map(self, cutted):
        '''
        Tdictionary (copy).csvODO
        这个方程用来将cutted后的string list，通过字典，变为数字表达形式。
        输入：
            分词后的字符串的列表，例如：["今天","天气","真好"]
        算法：
            利用self.dictionary.word2idx()得到字符在字典里对应的数字序号
            例如：
                今天 -> 10
                天气 -> 1293
                真好 -> 123
            无法识别的字符/字典里没有的： <UNK>

        输出：
            数字组成的列表，例如[10,1293,123]
        '''
        mapped = []
        for each_word in cutted:
            mapped.append(self.dictionary.word2idx(each_word))
        return mapped

    def pad(self, mapped, pad=2000):
        '''
        After mapping to num_list, we need to do padding,
        such that we would be able to use all models without getting trouble with
        dimensions.
        Input:
            mapped num_list
            pad              lenth you want to pad, set default = 2000
        output: padded num_list
        '''
        if len(mapped) >= 2000:
            return mapped[:2000]
        elif len(mapped) < 2000:
            _mapped = mapped.copy()
            _mapped.extend([0] * (2000 - len(_mapped)))
            return _mapped

    def embed(self, string, plantiff, defendant, third_party, pad = 2000):
        '''
        输入一段文字，对这一段文字进行分词+mapping处理
        :param:
            str() 需要输入的string
            pad: 你需要pad的max_len
        :return:
            np.array() 输出的embedding

        Notice that: 这一部分是每一个方法都不同的。
        '''
        # 首先调用transform进行预处理
        transformed = self.transform(string, plantiff, defendant, third_party)
        # print(transformed)
        # 分词
        cutted = self.cut(transformed)
        # print(cutted)
        # 然后进行map操作变为num_list
        num_list = self.map(cutted)
        # print(num_list)
        padded_list = self.pad(num_list, pad=pad)

        # 进行embed操作每个不同方法不同
        embedded = padded_list
        return embedded

    def embed_pandas(self, df, targets, plantiff="plantiff",
                     defendant="defendant", third_party="third_party", pad=2000):
        '''
        这个方程直接输入一个 dataframe,
        targets 是目标列的名字，可以有多个targets. target 必须是 list，即使只有一个！
        '''
        embedded_list = []
        for i in range(df.shape[0]):
            if i % 20 == 0:
                print("Doing", i, ". Total", df.shape[0])
            each_row_embed = []
            if type(targets) == str:
                # 说明只有一个输入的str
                embedded_list.append(self.embed(string=df.iloc[i][targets],
                                                     plantiff=df.iloc[i][plantiff],
                                                     defendant=df.iloc[i][defendant],
                                                     third_party=df.iloc[i][third_party]))
            else:
                # 多target模式
                for each_target in targets:
                    each_row_embed.append(self.embed(string=df.iloc[i][each_target],
                                                         plantiff=df.iloc[i][plantiff],
                                                         defendant=df.iloc[i][defendant],
                                                         third_party=df.iloc[i][third_party]))
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

    def embed(self, string, plantiff, defendant, third_party):
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
    '''
    This class is updated by Klaus.
    '''

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
