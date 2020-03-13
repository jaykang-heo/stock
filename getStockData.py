import pandas as pd
import pandas_datareader.data as pdr
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os


def get_url(item_name, code):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    df = pd.DataFrame()
    html = requests.get('{url}&page={page}'.format(url=url, page=1).replace(' ', '')).text
    soup = BeautifulSoup(html, 'lxml')
    end = soup.find('td',{'class':'pgRR'}).find('a')['href'].split('page=')[1]
    for page in range(1, int(end)):
        print(page)
        pg_url = '{url}&page={page}'.format(url=url, page=page).replace(' ', '')
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

data = pd.read_csv('rawStockCodes/kosdaqMkt.csv')
error = 0
errorList = []
for index, row in data.iterrows():
    code = str(row['종목코드'])
    name = row['회사명']
    # print(os.listdir('stocks'))
    if name+'.csv' in os.listdir('stocks'):
        continue
    if len(code)<6:
        code = '0'*(6-len(code))+code
    code += '.KQ'

    start = datetime(2000,1,1)
    end = datetime(2020,3,12)
    try:
        df = pdr.DataReader(code, 'yahoo', start, end)
        df['5일선'] = df['Close'].rolling(window=5).mean()
        df['8일선'] = df['Close'].rolling(window=8).mean()
        df['10일선'] = df['Close'].rolling(window=10).mean()
        df['30일선'] = df['Close'].rolling(window=30).mean()
        df['45일선'] = df['Close'].rolling(window=45).mean()
        df['60일선'] = df['Close'].rolling(window=60).mean()
        df['120일선'] = df['Close'].rolling(window=120).mean()
        df.to_csv('stocks/'+name+'.csv')
        print(code, name)
    except:
        error += 1
        errorList.append(name)
        print('error', code, name)







