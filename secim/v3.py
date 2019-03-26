import pandas as pd
from secim.constants import *

dfSelection = pd.read_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/dfSelection.pkl')

def readTuikData(path):
    myDf = pd.read_csv(path, sep=';', header=0)
    myDf = myDf.transpose()

    myDf['cityEng'] = [toeng(i) for i in myDf.index.values]
    myDf = myDf.set_index('cityEng')
    return myDf

path = '/home/cem/PycharmProjects/htmlParseInf/secim/lib.csv'
dfLib = readTuikData(path=path)
pathGsyh = '/home/cem/PycharmProjects/htmlParseInf/secim/gsyh.csv'
dfGsyh = readTuikData(path=pathGsyh)



df = dfSelection.join(dfLib, on='city')
df = df.set_index(['plaka', 'city'])

