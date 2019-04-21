
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
