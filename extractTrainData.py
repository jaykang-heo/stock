import pandas as pd

data = pd.read_csv('stocks/신라젠.csv')
del data['Unnamed: 0']

prev = ''
count = 0
for index, row in data[30:].iterrows():
    if index == 30:
        prev = row
    else:
        if 20 > (int(row['전일비'])/int(prev['종가']))*100 > 5 and prev['종가'] < row['종가']:
            tempData = data.iloc[index-30:index+2]
            if (data.iloc[index+2]['전일비']/data.iloc[index+1]['종가'])*100 >3:
                tempData['성공'] = 1
            else:
                tempData['성공'] = 0
            tempData.to_csv('trainData/'+str(count)+'.csv')
            count += 1
        prev = row