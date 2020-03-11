import pandas as pd
from bs4 import BeautifulSoup
import requests

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌

code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]
# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
print(len(code_df))

def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url
    # 신라젠의 일자데이터 url 가져오기

item_name='신라젠'
url = get_url(item_name, code_df)
# 일자 데이터를 담을 df라는 DataFrame 정의
df = pd.DataFrame()
# 1페이지에서 20페이지의 데이터만 가져오기
html = requests.get('{url}&page={page}'.format(url=url, page=1).replace(' ', '')).text
soup = BeautifulSoup(html, 'lxml')
end = soup.find('td',{'class':'pgRR'}).find('a')['href'].split('page=')[1]
for page in range(1, int(end)):
    pg_url = '{url}&page={page}'.format(url=url, page=page).replace(' ', '')
    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
# df.dropna()를 이용해 결측값 있는 행 제거
df = df.dropna()
# 상위 5개 데이터 확인하기

data = df[::-1]
data['5일선'] = data['종가'].rolling(window=5).mean()
data['8일선'] = data['종가'].rolling(window=8).mean()
data['10일선'] = data['종가'].rolling(window=10).mean()
data['30일선'] = data['종가'].rolling(window=30).mean()
data['45일선'] = data['종가'].rolling(window=45).mean()
data['60일선'] = data['종가'].rolling(window=60).mean()
data['120일선'] = data['종가'].rolling(window=120).mean()

print(data.to_csv('stocks/신라젠.csv'))
data.to_csv('stocks/'+item_name+'.csv')
print(data)

