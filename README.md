# sufelaw2019
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


# law package 介绍

clone 了这个repository后，使用 import 来调用这个包
~~~
import law
~~~

下面是这个包的一些介绍。

## law.utils 包

这个包集成了你所需要的很多分词工具，例如从一段文字中直接提取法律名、条款号。

### 调用包
包里主要有以下两个方程：
~~~
from law.utils import find_law_in_series
from law.utils import find_law_tiao_kuan_in_text
~~~

### 对一段文字调用包
~~~
>>> find_law_tiao_kuan_in_text("据此，根据《中华人民共和国保险法》第六十五条第二、三款、《中华人民共和国民事诉讼法》第六十四条第一款、第一百四十四条规定，判决如下:一、被告中国平安财产保险股份有限公司上海分公司、被告中国平安财产保险股份有限公司应于本判决生效之日起十日内支付原告冷桂芝保险金人民币888,022.80元；二、原告冷桂芝其他诉讼请求不予支持。、如果未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由被告平安保险公司、平安保险上海分公司共同负担。")

# output:
[['《中华人民共和国保险法》', ['第六十五条'], ['第六十五条第二、三款']],
['《中华人民共和国民事诉讼法》', ['第六十四条', '第一百四十四条', '第二百五十三条'], ['第六十四条第一款']]]
~~~

### 在一个Pandas Series上调用包
提取这个series里所有的法律名称，条款号，返回一个同样长度的list，list中元素和$find_law_tiao_kuan_in_text$一致
~~~
find_law_in_series(data['法院意见'])
~~~

## law.preprocessing包

这个包是我们最后需要写成的模块集合，可以对号入座！
