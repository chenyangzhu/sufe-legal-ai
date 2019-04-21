## law.dictionary
所有的字典都通过主类base_class建立，字典的源文件存储在`'./law/dict/`当中，字典必须用`utf-8`存储为`csv`格式。
#### `base_class` law.dictionary.Dictioanry()
这是所有dictionary文件的母函数，主要提供以下几个方程：
- 函数：
  - `word2idx(word:str) -> int` 输入字符串，返回在字典里对应的序号
  - `idx2word(idx:int) -> str` 输入序号，返回字符串
- 变量：
  - `sign` 返回所有标点符号的列表(list)
  - `dict_len` 返回字典长度
