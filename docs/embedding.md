# Embedding

在Embedding中，我们构建从字符串到embedding的全部流程，这一部分将作为我们文本处理最重要的构建。
有大量的utils文件用来辅助这一部分的运作。

我们首先建立了一个主类`Embedding`，用来统一和指导所有的对象处理。


## `class` law.embedding.Embedding(dict_dir, jieba_dict)
Embedding 主类是我们做所有项目所需要的一切基础，这里将会详细介绍所有运用到的方法，和如何调用API

### Input
Embedding需要输入两个变量
- `dict_dir` 用来输入我们存放字典的地址，默认为`./law/dict/dictionary.csv`
- `jieba_dict` 用来为给jieba分词，我们常用的词汇，其实就是上述dict的txt版本

### 流程
embedding部分的所有操作如下所示：
```
# 对任意一条数据文本

# Entity Identification
transformed = self.transform(string, plantiff, defendant, third_party)

# 分词
cutted = self.cut(transformed)

# 利用字典map到num list
num_list = self.map(cutted)

# padding到规整
padded_list = self.pad(num_list, pad=PAD)
```
所有流程全部放置到`self.embed()`中，之后只需要调用以下api即可处理
```
mtd = law.embedding.Embedding("./law/dict/dictionary.csv", "./law/dict/jieba_dict.txt")
num_list = mtd.embed_pandas(df=data,targets = "process")
```
其中，我们的dataframe叫做`data`，目标处理列叫做`process`。


### Functions
#### `transform()`
这一部分，主要做的是 entity identification. 全局预处理，将所有包含以下字符的信息，转换为后面的符号。
```
'地名': PLA
'原告': PLT
'被告': DFD
'第三人': THP
'标点符号': 直接删除
'数字': NUMBER
```
输入：
- `string` str() 需要切词的文件
- `plantiff` str() 各个被告，用‘、’连接（就是数据库里的那一列）
- `defendant` str() 各个元告，用'、'连接
- `third_party` str() 各个第三人，用'、'连接

输出：
transformed string

注意：
- 如果不想要输入`plantiff`，`defendant`，`third_party`的信息，可以直接不输入。

#### `cut(transformed)`
目前使用结巴分词分词，之后可以更改
character-level model 不需要分词
TODO 可能需要手动把大写英语字母切开


### `map(cutted)`
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


### `pad(mapped, pad=2000)`
After mapping to num_list, we need to do padding,
such that we would be able to use all models without getting trouble with
dimensions.

Input:
- mapped num_list
- pad              lenth you want to pad, set default = 2000

Output:
- padded num_list


### `embed(self, string, plantiff='', defendant='', third_party='', pad = 2000)`
输入一段文字，对这一段文字进行分词+mapping处理

输入:
- str() 需要输入的string
- pad: 你需要pad的max_len

输出：
- np.array() 输出的embedding

Notice that: **这一部分是每一个方法都不同的，之后的不同方法，全都写在这里。**

### `embed_pandas(self, df, targets, plantiff="plantiff", defendant="defendant", third_party="third_party", pad=2000)`
自动对一个pandas dataframe处理
输入：
- `df` 想要处理的Dataframe
- `targets` 目标NLP列
- `plantiff` 原告列名
- `defendant` 被告列名
- `third_party` 第三人列名
- `pad` padding的长度


# `class` char_freq

# `class` TFIDF

# `class` BERT
