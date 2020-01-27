from datetime import datetime
import pandas_datareader.data as wb
import pandas as pd

start = datetime(1950, 10, 2)
end = datetime(2021, 1, 1)
#


def saveStockCode():
    url_market = ['kosdaqMkt', 'stockMkt']
    for i in url_market:
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % i
        df = pd.read_html(url, header=0)[0]
        df[['회사명', '종목코드']].to_csv(i+'.csv')


if __name__ == '__main__':
    # saveStockCode()
    data = pd.read_csv('kosdaqMkt.csv')
    for j,i in zip(data['회사명'],data['종목코드']):
        name = str(i)+'.KS'
        df = wb.DataReader('035420.KS', 'yahoo', start, end)
        print(len(df))
        # df.to_csv(j+'csv')
