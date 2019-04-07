# 智能法务系统官方文档

## 特点
- 提供终审预测系统
- 提供法条推荐系统
- MIT 授权协议


# law package 介绍

## law.data
#### `class` law.data.read_law(n=1000, preprocessing=False)
- `return_data()` 提取data
- `store()` 存储data到本地

## law.model
#### `class` law.model.basemodel()
所有的model都使用了basemodel作为底层，实现以下功能：
- `fit(X,y)`
- `predict(X)`
- `store()` 存储已经训练过的模型
- `read()`读取先前训练过的模型

## law.nlp
#### law.nlp.TFIDF(string)
计算某段文字中的TFIDF统计量。

## law.dictionary
TODO 用来存放构建字典的代码，和频率文件。

## law.utils

#### law.utils.find_law_in_series(string)
查找一个 pandas DataFrame 一列每一行的法条
~~~
find_law_in_series(data['opinion'])
~~~
#### law.utils.find_law_tiao_kuan_in_text()
查找一段string里的所有法条
~~~
>>> find_law_tiao_kuan_in_text("据此，根据《中华人民共和国保险法》第六十五条第二、三款、《中华人民共和国民事诉讼法》第六十四条第一款、第一百四十四条规定，判决如下:一、被告中国平安财产保险股份有限公司上海分公司、被告中国平安财产保险股份有限公司应于本判决生效之日起十日内支付原告冷桂芝保险金人民币888,022.80元；二、原告冷桂芝其他诉讼请求不予支持。、如果未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由被告平安保险公司、平安保险上海分公司共同负担。")

# output:
[['《中华人民共和国保险法》', ['第六十五条'], ['第六十五条第二、三款']],
['《中华人民共和国民事诉讼法》', ['第六十四条', '第一百四十四条', '第二百五十三条'], ['第六十四条第一款']]]
~~~
#### law.utils.find_something_with_pre()
#### law.utils.classify_subject_in_text()
#### law.utils.getn()
#### law.utils.ADBinfo()
#### law.utils.total_fa_tiao_kuan()

## law.entity_extractor
用于对法人和非法人组织进行分类，主要判别参照：http://www.sohu.com/a/249531167_656612
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
