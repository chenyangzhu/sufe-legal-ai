# 智能法务系统官方文档

## 特点
- 提供终审预测系统
- 提供法条推荐系统
- MIT 授权协议

## 安装说明
代码对 Python 2/3 均兼容
- 全自动安装：easy_install law 或者 pip install law / pip3 install law
- 手动安装：将 law 目录放置于当前目录或者 site-packages 目录
- 通过 import law 来引用

## 模型思路

- SVD 分解
  - 行：案件 列：特征
  - 对于共线性的解释 (奇异值小的）
  - 可以预测没有观测的位置的取值

- logistic 回归（筛选变量之后）可以尝试其他连接函数
  先用主成分分解看变量相依关系

- 贝叶斯网络-> conditional probability between feature

  可能要先做特征筛选

  实现方法

   https://site.douban.com/182577/widget/notes/12817482/note/273585095/

  R包 gRain bnlearn
  
 - 随机森林模型
   通过训练结果筛选出强特征
 
 - 多标签分类模型
   - LPLR模型
     将每个标签组合看作是一个标签，转化成标签之间互相独立的多标签分类问题
   - LBR模型
     划分标签空间，减少枚举和运算
 

## law package 介绍

clone 了这个repository后，使用 import 来调用这个包
~~~
import law
~~~

下面是这个包的一些介绍。

### law.utils 包

这个包集成了你所需要的很多分词工具，例如从一段文字中直接提取法律名、条款号。

#### 调用包
包里主要有以下两个方程：
~~~
from law.utils import find_law_in_series
from law.utils import find_law_tiao_kuan_in_text
~~~

#### 对一段文字调用包
~~~
>>> find_law_tiao_kuan_in_text("据此，根据《中华人民共和国保险法》第六十五条第二、三款、《中华人民共和国民事诉讼法》第六十四条第一款、第一百四十四条规定，判决如下:一、被告中国平安财产保险股份有限公司上海分公司、被告中国平安财产保险股份有限公司应于本判决生效之日起十日内支付原告冷桂芝保险金人民币888,022.80元；二、原告冷桂芝其他诉讼请求不予支持。、如果未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由被告平安保险公司、平安保险上海分公司共同负担。")

# output:
[['《中华人民共和国保险法》', ['第六十五条'], ['第六十五条第二、三款']],
['《中华人民共和国民事诉讼法》', ['第六十四条', '第一百四十四条', '第二百五十三条'], ['第六十四条第一款']]]
~~~

#### 在一个Pandas Series上调用包
提取这个series里所有的法律名称，条款号，返回一个同样长度的list，list中元素和$find_law_tiao_kuan_in_text$一致
~~~
find_law_in_series(data['法院意见'])
~~~

### law.entity_extractor包

这个包主要用于对法人和非法人组织进行分类
主要判别参照：http://www.sohu.com/a/249531167_656612

#### 调用包
包里主要有以下方程：
~~~
from law.entity_extractor import Entity_Extractor
~~~

#### 对一段文字调用包
~~~
>>> find_law_entity_extractor("据此，根据《中华人民共和国保险法》第六十五条第二、三款、《中华人民共和国民事诉讼法》第六十四条第一款、第一百四十四条规定，判决如下:一、被告中国平安财产保险股份有限公司上海分公司、被告中国平安财产保险股份有限公司应于本判决生效之日起十日内支付原告冷桂芝保险金人民币888,022.80元；二、原告冷桂芝其他诉讼请求不予支持。、如果未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由被告平安保险公司、平安保险上海分公司共同负担。")

# output:
原告 ['二、冷桂芝其他诉讼请求不予支持' '冷桂芝保险金人民币888,022.80元；二、'
 '冷桂芝其他诉讼请求不予支持。、如果未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由']
被告 ['由平安保险公司、平安保险上海分公司共同负担' '中国平安财产保险股份有限公司上海分公司、'
 '中国平安财产保险股份有限公司应于本判决生效之日起十日内支付' '平安保险公司、平安保险上海分公司共同负担。']
0
Dumping model to file cache /var/folders/6g/28dh6l2j7v7bv8wdk1jct2m40000gn/T/jieba.cache
Loading model cost 1.210 seconds.
Prefix dict has been built succesfully.
0
~~~

### law.preprocessing包

这个包集成了我们所写成的针对案例数据特征进行分词预处理工具

#### 调用包
包里主要有以下方程：
~~~
from law.preprocessing import numberx(self)
~~~

#### 主要实现功能
- number1 标题：法案标题
- number2 案号：法案系统编号
- number3 案件类型：提取案件类型“民事”或“刑事”
- number4 庭审程序：
- number5 案由：提取40种案件分类
- number6 文书类型：分类“判决书”或“裁定书”
- number7 法院：分类院所在地及等级
- number8 判决日期：拆分判决日期为“年”、“月”、“日”
- number9 原告：分类原告的组成
- number10 被告：
- number11 第三人：按是否为自然人分类第三人的组成
- number12 法官：
- number13 审判长：
- number14 审判员：
- number15 书记员：
- number16 头部：
- number17 当事人：
- number18 庭审程序说明：
- number19 庭审过程：
- number20 法院意见：按是否涉及金额分类法院意见
- number21 判决结果：按判决法条及赔偿结果拆分判决结果
- number22 庭后告知：按是否终审分类庭后告知为0，1变量
- number23 结尾：
- number24 附录：




## 模型思路
> An awesome project.

**这个是加粗**

*这个是斜体*

这个是列表
* 一二三
* 四五六

# 这是第二个主标题

通过这个写小的代码
`this is how you write codes`

或者写代码的block
~~~
python law.py

~~~

# 更多的参考内容

- markdown 教程链接[link](https://en.support.wordpress.com/markdown-quick-reference/)
- documentation生成器[link](https://docsify.js.org/#/quickstart)
