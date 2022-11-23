import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime

with open('전기차_부정어.txt', encoding='utf-8') as neg:
    negative = neg.readlines()

with open('전기차_긍정어.txt', encoding='utf-8') as pos:
    positive = pos.readlines()

negative = [neg.replace('\n', '') for neg in negative]
positive = [pos.replace('\n', '') for pos in positive]

# my_title_dic = {"date":[],"title":[]}
d = datetime.date(2018, 1, 1)
today = datetime.date(2019,1,1)

date_list = []
titles_list = []
labels_list = []
j = 0

while (not d == today):
    year = "{:%Y}".format(d)
    month = "{:%m}".format(d)
    day = "{:%d}".format(d)
    print(d)
    for i in range(20):
        num = i * 10 + 1
        # 전기차
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EC%A0%84%EA%B8%B0%EC%B0%A8&sort=2&photo=3&field=0&pd=3&ds=" + str(
            year) + '.' + str(month) + '.' + str(
            day) + "&de=2022.05.15&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:from" + str(
            year) + str(month) + str(day) + 'to' + str(year) + str(month) + str(day) + ",a:all&start=" + str(num)

        req = requests.get(url)

        soup = BeautifulSoup(req.text, 'lxml')

        titles_iter = soup.select("a.news_tit")

        for title in titles_iter:
            title_data = title.text
            clean_title = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\|\(\)\[\]\<\>`\'…\"\"》]', '', title_data)
            negative_flag = False
            label = 0

            for i in range(len(negative)):
                if negative[i] in clean_title:
                    label = -1
                    negative_flag = True

                    print('negative 비교단어 : ', negative[i], 'clean_title : ', clean_title)
                    break
            if negative_flag == False:
                for i in range(len(positive)):
                    if positive[i] in clean_title:
                        label = 1

                        print('positive 비교단어 : ', positive[i], 'clean_title', clean_title)
                        break
            titles_list.append(title_data)
            date_list.append(d)
            labels_list.append(label)

    # print(len(my_title_dic['title']))
    d += datetime.timedelta(+1)

my_title_df = pd.DataFrame({'date': date_list, 'title': titles_list, 'label': labels_list})
print(my_title_df)


def dftoCsv(my_title_df):
    my_title_df.to_csv(('전기차여론_2018.csv'), sep=',', index=False, na_rep='NaN', encoding='utf-8-sig')


dftoCsv(my_title_df)