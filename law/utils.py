import re
import pandas as pd


def find_law_in_series(series):
    '''
    Input:
        Pandas Series

    Output:
        Law and its tiao and kuan
        First layer: Iterate through all rows in the Pandas Series
        Second layer: ['law',['tiao','tiao',...],[kuan,kuan,kuan,...]]
    '''

    data_len = len(series)
    findings = []

    for i in range(data_len):
        if pd.isnull(series.iloc[i]):
            findings.append([])
            continue
        findings.append(find_law_tiao_kuan_in_text(series.iloc[i]))
    return findings


def find_law_tiao_kuan_in_text(string):
    '''
    Given a text containing law, tiao and kuan.
    Sample Input:
    据此，根据《中华人民共和国保险法》第六十五条第二、三款、《中华人民共和国民事诉讼法》
    第六十四条第一款、第一百四十四条规定，判决如下:一、被告中国平安财产保险股份有限公司
    上海分公司、被告中国平安财产保险股份有限公司应于本判决生效之日起十日内支付原告冷桂芝
    保险金人民币888,022.80元；二、原告冷桂芝其他诉讼请求不予支持。、如果未按本判决指定
    的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加
    倍支付迟延履行期间的债务利息。、案件受理费12,734.90元，减半收取计6,367.45元，由被
    告平安保险公司、平安保险上海分公司共同负担。

    Sample Output:
    [['《中华人民共和国保险法》', ['第六十五条'], ['第六十五条第二、三款']],
    ['《中华人民共和国民事诉讼法》', ['第六十四条', '第一百四十四条', '第二百五十三条'], ['第六十四条第一款']]]

    Notice:
    保留了款前的条，是因为这样更加方便，更加快捷。
    '''

    final_list = []

    # We first find these "< >"
    sign_find = re.compile(r"《.*?》")

    # We use these names to refind the tiaokuan
    law_list = re.findall(sign_find, string)
    law_set = set(law_list)
    law_length = len(law_set)

    if law_length > 0:  # only do the following when the list is not empty

        # We do this because it's hard to match the law and its tiaokuan.
        for j in range(law_length):
            thislaw = law_set.pop()
            tiao_finder = re.compile(thislaw+r"第.*?条.*?(?:《|。|$)")
            tiao = re.findall(tiao_finder, string)
            # Notice that there might be same laws many times

            real_tiao_list = []
            kuan_list = []

            if len(tiao) > 0:
                for k in range(len(tiao)):
                    if len(tiao[k]) > 0:
                        # Assume that no more than 5 between tiao
                        tiao_finder_plus = re.compile(r"第.{1,5}条")
                        real_tiao = re.findall(tiao_finder_plus, tiao[k])
                        real_tiao_list.extend(real_tiao)

                        for p in range(len(real_tiao)):
                            kuan_finder = re.compile(real_tiao[p]+"第.{1,5}款")
                            kuan = re.findall(kuan_finder, tiao[k])
                            kuan_list.extend(kuan)
            final_list.append([thislaw, real_tiao_list, kuan_list])
    return final_list


def find_something_with_pre(pre, find, string):
    '''
    pre add find - all strings
    '''
    crit = re.compile(pre+".*?"+find)
    all_result = re.findall(crit, string)
    return all_result[0]
