import pandas as pd
from BilancoParse.constants import *

stocks = Bist30Stocks
periods = [
    '2016_1', '2016_2', '2016_3', '2016_4',
    '2017_1', '2017_2', '2017_3', '2017_4',
    '2018_1', '2018_2', '2018_3', '2018_4'
]


def getMistakes(data):
    SubCodeUnique = set(data['LastSubCode'].values)
    mistakeSubCodes = []
    for i in SubCodeUnique:
        if type(i) == str:
            j = int(i[:-1])
            subTotal = sum(data.loc[data['LastSubCode'] == i, 'colDipToplam'])
            checkTotal = data.loc[data['tableindex'] == j, 'colDipToplam'].values
            if checkTotal[0] - subTotal != 0:
                print(i)
                print(checkTotal)
                print(subTotal)
                mistakeSubCodes.append(i)
            else:
                pass
                print('{} => Dogru, checkTotal => {} subTotal=> {}'.format(i, checkTotal, subTotal))
    return mistakeSubCodes


years = [2016, 2017, 2018]

for year in years:

d = []
for stock in stocks:
    for period in periods:
        try:
            path = '/home/cem/Desktop/diptoplamChecks/pickles/{}_{}_PartB.pkl'.format(stock, period)
            df = pd.read_pickle(path)
        except Exception as e:
            print('{} {} bulunamadi.'.format(stock, period))
            continue
        mistakeSubCodes = getMistakes(data=df)
        if len(mistakeSubCodes) > 0:
            d.append({'period': period, 'stock': stock, 'mistakes': mistakeSubCodes})
            print('{} yanlis calculation bulundu', stock)
