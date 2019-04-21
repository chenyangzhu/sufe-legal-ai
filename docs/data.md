
## law.data
这一个模块主要用来处理所有的数据，包括连接数据库的形式调用数据、数据预处理等。


#### `class` law.data.case_reader(n=1000, preprocessing=False)
用来读取案件，
- 输入:
  - `n` 你想要读取的案件数目
  - `preprocessing` 是否需要预处理
- 函数
  - `law.data.case_reader.return_data()` 提取data，返回 pandas Dataframe
  - `store()` 存储data到本地，默认地址为"./cache/"

#### `class` law.data.law_reader()
用来读取法律，
- 函数：
  - `return_full_law(law_name)`
    - 输入：
    - `law_name`是你想要查询的法律的英语名，目前提供以下两个
      - 中华人民共和国合同法 - contract
      - 中华人民共和国劳动法 - labor
    - 输出：
      - pandas.dataframe 储存这条法律的所有信息，包括tag等
  - `query(law_name)`
    - 输入：
      - `law_name`是你想要查询的法律的英语名
    - 输出：
      - dictionary [index，tag1，tag2，tag3，tag4，tag5，article]
- 用法
```
rd = law.data.law_reader() # 生成reader对象
rd.return_full_law("labor") # 查询劳动法
rd.query("labor",10) # 查询劳动法第十条
```
