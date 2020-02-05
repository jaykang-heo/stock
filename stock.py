from datetime import datetime
import pandas_datareader.data as wb
import pandas as pd

# start = datetime(1970, 1, 1)
start = datetime(2019, 1, 1)
end = datetime(2019, 2, 1)


def saveStockCode():
    url_market = ['kosdaqMkt', 'stockMkt']
    for i in url_market:
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=%s' % i
        df = pd.read_html(url, header=0)[0]
        df[['회사명', '종목코드']].to_csv(i+'.csv')


def readStock():
    data = pd.read_csv('kosdaqMkt.csv')
    error = 0
    success = 0
    df = wb.DataReader('257370.KQ', 'yahoo', start, end)
    print(df)
    print(len(df))
    # for name, code in zip(data['회사명'], data['종목코드']):
    #     if len(str(code))<6 : code=(6-len(str(code)))*'0'+str(code)
    #     code = str(code) + '.KQ'
    #     print(code)
    #     try:
    #         df = wb.DataReader(code, 'yahoo', start, end)
    #         success+=1
    #         print(name, code, len(df))
    #     except:
    #         error +=1
    #         print("error")
    # print("total codes: ",success, "total error: ", error)
        # df.to_csv(j+'csv')


if __name__ == '__main__':
    # saveStockCode()
    readStock()
