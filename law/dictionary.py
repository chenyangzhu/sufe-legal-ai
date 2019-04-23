import numpy as np
import pandas as pd

class Dictionary:
    def __init__(self, dict_dir):
        '''
        算法要求：必须使用哈希列表 Hash Table，实在不行用dict()写。
        注意：绝对不可以用Dataframe的查找来写。
        在 init 里阅读文档中的字典文件，注意要把地名等字典都融合到一起。
        '''
        self.data = pd.read_csv(dict_dir,encoding="UTF8")

        print("Building Dictionary from ", dict_dir)
        self._word2idx = {}
        self._idx2word = {}
        for i in range(len(self.data)):
            self._word2idx[self.data[i]['word']] = self.data[i]['index']
            self._idx2word[self.data[i]['index']] = self.data[i]['word']

    @property
    def dict_len(self):
        assert len(self.word2idx) == len(self.idx2word)
        return len(self.word2idx)

    @property
    def sign(self):
        return ['，', '？', '！', '、', '—',
                '“', '”', '；', '。', '|', '{', '}',
                '《', '》', '.', ',', '<', '>', ':', '：', '）', '（']

    def word2idx(self, word):
        try:
            return self._word2idx[word]
        except KeyError:
            return self._word2idx["UNK"]

    def idx2word(self, idx):
        try:
            return self._idx2word[idx]
        except KeyError:
            return "UNK"

class City(Dictionary):
    def __init__(self, dict_dir):
        '''
        这个字点专门用来存储地点和城市，输入的地址需要是城市文件的地址
        默认在law/dict/places.csv
        这个文件里有五列，分别为
        index	word	region	area	province
        序号     城市名   地区     大区    省份
        4       上海市   苏皖沪    东区    上海市
        城市叫 word 的原因是为了与主函数同步
        '''
        super().__init__(dict_dir)

    def idx2city(self, idx):
        # 这两个方程是等价的
        return self.idx2word(idx)

    def city2idx(self, city):
        # 这两个方程是等价的
        return self.word2idx(city)

    def city2province(self, city):
        # TODO 城市转换为省份
        return 0

    def city2region(self, city):
        # TODO 城市转为大区
        return 0
