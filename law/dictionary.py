import numpy as np
import pandas as pd

place = ['郑州', '沈阳', '深圳', '广西', '广州', '乌鲁木齐','苏州','粤','南京',
             '江苏','江南','南宁','华东','益州','沪东','福建','奉贤','亚洲','甘肃',
             '泰安','东营','蒙','粤北','淮南','京西','连云港','江西','临沂']

class Dictionary:
    def __init__(self, dict_dir):
        '''
        算法要求：必须使用哈希列表 Hash Table，实在不行用dict()写。
        注意：绝对不可以用Dataframe的查找来写。
        在 init 里阅读文档中的字典文件，注意要把地名等字典都融合到一起。
        '''
        self.data = pd.read_excel(path)
        self.dict_dir = dict(map(lambda x,y:[x,y], self.data['index'],self.data['word'])) 
        self.data_len = len(self.data)
        for key, val in self.dict_dir.items():
            for j,words in enumerate(place):
                if val == data_list[j]:
                    self.dict_dir[key] = '地区'

    @property
    def sign(self):
        return ['，', '？', '！', '、', '—',
                '“', '”', '；', '。', '|', '{', '}',
                '《', '》', '.', ',', '<', '>', ':', '：', '）', '（']

    def string2idx(self, string):
        '''
        TODO
        I/O 要求：输入一个字符，返回一个他在字典里的序号

        :param:
            string str() 我要查找的字符
        :return:
            idx int() 字符在字典里的序号
        '''
        for key, val in self.dict_dir.items():
            if val == string:
                print("符号在字典里对应的字符 : %d" % key)

    def idx2string(self, idx):
        '''
         TODO
         I/O 要求： 输入一个序号，返回他在字典里对应的字符

         :param:
            idx int() 序号
        :return:
            string str() 字典里对应的字符
        '''
        print ("字符在字典里的序号 : %s" % self.dict_dir.get(idx))

if __name__ == "__main__":
    test = Dictionary('.../dict.xlsx',place)
    test.string2idx()
    test.idx2string()
