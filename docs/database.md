# 数据库概览(private)

我们的数据库布置在腾讯云上，地址是
```
{
  user="你的名字拼音",
  password=“law”+"你的名字拼音",
  host="cdb-74dx1ytr.gz.tencentcdb.com",
  port = "10008",
}
```
例如：user="zhuchenyang", password="law-zhuchenyang"。注意这个帐号并不存在。
> Warning: Do not expose user and password to anyone.

## 连接数据库
### 使用终端（cmd/terminal）连接
你可以阅读腾讯云的[简介](https://cloud.tencent.com/document/product/236/3130)，即可使用。简而言之，首先是安装mysql，然后在cmd/terminal中输入，
```
mysql -h cdb-74dx1ytr.gz.tencentcdb.com -P 10008 -u root -p
```
### 使用python连接
在python里，主要的使用方式是用以下语句，使用mysql包，或者pymysql都可以，这里用mysql作为简介。

```
import mysql.connector
import pandas as pd

# 连接数据库
cnx = mysql.connector.connect(user="user", password="password",  # 注意修改
                              host="cdb-74dx1ytr.gz.tencentcdb.com",
                              port = "10008",
                              database="law")
cursor = cnx.cursor(buffered=True)

# 通过pandas阅读数据库内容
data = pd.read_sql('SELECT * FROM Civil;',con=cnx)
```


## 数据库的构造
我们的数据库目前还比较混乱，主要使用的是以下结构
目前这个数据库里有一个库叫做`law`，这个库里有一个表叫做`Civil`，数据库的默认编码是`utf8`，所有的配置可以在群里查看。`Civil`的primary key和索引都是`id`，也就是案号，其他的都可以为空。
```
├── law
|    └── Civil
├── law_article
    ├── contract
    └── labor
```
其中`law`存放的是所有案件，`Civil`代表民事。而`law article`则指的是法律原文，其中contract和labor分别指代《合同法》和《劳动法》。

### `Civil`表
目前`Civil`中有7w+数据，所有行和excel对应如下，
```
{'标题': 'title',
 '案号': 'id',
 '案件类型': 'type',
 '庭审程序': 'proc',
 '案由': 'class',
 '文书类型': 'doc_type',
 '法院': 'court_name',
 '判决日期': 'date',
 '原告': 'plantiff',
 '被告': 'defendant',
 '第三人': 'third_party',
 '法官': 'judge',
 '审判长': 'judge_chief',
 '审判员': 'judge_board',
 '书记员': 'writer',
 '当事人': 'party',
 '庭审程序说明': 'procedure',
 '庭审过程': 'process',
 '法院意见': 'opinion',
 '判决结果': 'result',
 '庭后告知': 'notice',
 '附录': 'appendix'}
```

## 上传现有的数据
在项目根目录`upload.py`文件，可以简单地处理并上传所有的数据，在 command line / cmd / terminal 定位到本项目的目录。
```
python upload.py --dir='输入你存放数据的文件夹例如：./data' --u=root --p=sufelaw2019
```
- 注意1：在你存放数据的文件夹里，只能有需要上传的excel文件，不要存放任何其他文件，之后根据该程序的操作即可完成数据上传。
- 注意2：程序将自动对数据进行如下预处理，
  - 对所有的nan用""替换；
  - 对没有时间的条目，用'2050-01-01'替换；
  - 合并了重复的列，使用简单的字符串加减;
  - 更改了列名，为了配合MySQL的名称
- 注意3：上传时会自动跳过重复条目、overflow条目等。
- 注意4：如果发生bug等任何问题，请及时提交issue在github上！
