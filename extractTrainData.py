import pandas as pd
import os

df = pd.read_csv('stocks/하츠.csv')
prevClose = df.iloc[0]['Close']
curClose = df.iloc[1]['Close']
prev = ''
count = 0

for file in os.listdir('stocks'):
    data = pd.read_csv('stocks/'+file)
    # del data['Unnamed: 0']

    prev = ''
    success = 0
    fail = 0
    count = 0
    for index, row in data[30:].iterrows():
        if index == 30:
            prev = row
        else:
            diff = abs(int(prev['Close']) - int(row['Close']))
            count+=1
            percent = round(diff/int(prev['Close'])*100, 2)
            if 20 > percent > 5 and prev['Close'] < row['Close']:
                print(percent, prev['Close'], row['Close'])
                tempData = data.iloc[index-30:index+2]
                if (data.iloc[index+1]['Close']/data.iloc[index+2]['Close'])*100 >3:
                    tempData['Success'] = 1
                    success += 1
                else:
                    tempData['Success'] = 0
                    fail += 1
                tempData.to_csv('trainData/'+str(count)+'.csv')
                count += 1
            prev = row

            # print(file, count, "success:", success, "/ fail:", fail)