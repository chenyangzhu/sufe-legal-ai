# 智慧法务系统
> AI + 大数据赋能法务智能

官方文档[链接](https://chenyangzhu.github.io/sufelaw2019/)


## 直接调用law.data读取数据库数据
为了简单方便使用数据库资源，我们已经把连接数据库的部分全部整合到了`law.data`，也就是原先的
`law.preprocessing`当中。你可以使用如下的方式调用，
```
data = law.data.law_reader(n=1000,prerprocessing=True).return_data()
```
将读取数据库中的前1000条数据，并自动进行预处理。当然，也可以选择不进行预处理，则勾选False。
preprocessing默认为False。之后将开放选择类别等其他选项。

## 也可以使用如下方式连接MySQL
由于初次做项目的时候发现数据存在大量的不容和、所有人数据版本不同的情况，我们建立了一个非常容易使用的MySQL server，你可以直接通过MySQL对该服务器进行访问。

之后将删除github里的所有数据。
### 如何上传我现有的数据？
我已经在项目根目录写了一个`upload.py`文件，可以简单地处理并上传所有的数据，在 command line / cmd / terminal 定位到本项目的目录。
```
python upload.py --dir='输入你存放数据的文件夹例如：./data' --u=root --p=sufelaw2019
```
- 注意1：在你存放数据的文件夹里，只能有需要上传的excel文件，不要存放任何其他文件，之后根据该程序的操作即可完成数据上传。
- 注意2：程序将自动对数据进行如下预处理，
  - 对所有的nan用""替换；
  - 对没有时间的条目，用'2050-01-01'替换；
  - 合并了重复的列，使用简单的字符串加减;
  - 更改了列名，为了配合MySQL的名称.
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
- 注意3：上传时会自动跳过重复条目、overflow条目等。
- 注意3：如果发生bug等任何问题，请及时提交issue在github上！

### 我如何调用服务器里的数据？
你可以阅读腾讯云的[简介](https://cloud.tencent.com/document/product/236/3130)，即可使用。简而言之，首先是安装mysql，然后在cmd/terminal中输入，
```
mysql -h cdb-74dx1ytr.gz.tencentcdb.com -P 10008 -u root -p
```
当然在python里，主要的使用方式是用以下语句，使用mysql包，或者pymysql都可以，这里用mysql作为简介。
```
import mysql.connector
import pandas as pd

# 连接数据库
cnx = mysql.connector.connect(user="root", password="sufelaw2019",
                              host="cdb-74dx1ytr.gz.tencentcdb.com",
                              port = "10008",
                              database="law")
cursor = cnx.cursor(buffered=True)

# 通过pandas阅读数据库内容
data = pd.read_sql('SELECT * FROM Civil;',con=cnx)
```
### 数据库的构造
目前这个数据库里有一个库叫做`law`，这个库里有一个表叫做`Civil`，数据库的默认编码是`utf8`，所有的配置可以在群里查看。`Civil`的primary key和索引都是`id`，也就是案号，其他的都可以为空。


## 使用UI界面

在目录`page`下，在cmd/terminal输入
```
python manage.py runserver
```
随后在浏览器里输入以下地址
```
localhost:8008/admin/
```
输入账户`root`和密码`123456`，即可存储法律文件。
