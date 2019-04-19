import pandas as pd
from BilancoParse.constants import *


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


def getPeriods(years):
    periods = []
    for y in years:
        for quarter in range(1, 5):
            periods.append('{}_{}'.format(y, quarter))
    return periods


def getTotalMistakes(stocks, periods):
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
    return d

def getSP(years, konsolide_f):
    d = {'{}_{}'.format(y, d): [] for y in years for d in [1, 2, 3, 4]}
    for year in years:
        if konsolide_f:
            data = pd.read_pickle('/home/cem/PycharmProjects/htmlParseInf/outputs/t/B2/{}_1234_B_k.pkl'.format(year))
        if not konsolide_f:
            data = pd.read_pickle('/home/cem/PycharmProjects/htmlParseInf/outputs/t/B2/{}_1234_B.pkl'.format(year))
        data['periodStock'] = data['period'] + ";" + data['stock']
        stocksperiods = data['periodStock'].unique()
        pSlist = list(map(lambda x: x.split(';'), stocksperiods))
        for p, s in pSlist:
            d[p].append(s)
    return d


def getNullSP(years, Bist30Stocks=Bist30Stocks, konsolide_f=1):
    sP = getSP(years=years, konsolide_f=konsolide_f)

    n = {}
    for p, sList in sP.items():
        nullStocks = [s for s in Bist30Stocks if s not in sList]
        n[p] = nullStocks
    return n


years = [2016, 2017, 2018]
periods = getPeriods(years=years)
stocks = Bist30Stocks
totalMistakes = getTotalMistakes(stocks=stocks, periods=periods)
