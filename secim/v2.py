from secim.constants import *

import pickle


def read_pickle(path):
    pkl_file = open(path, 'rb')
    myDict = pickle.load(pkl_file)
    return myDict


def getPartySymbol(argDict, headers):
    for city, values in argDict.items():
        # parti sembolunu cekiyoruz
        partySymbol = [header for header in headers if values in header][0][0]
        argDict[city] = partySymbol
    return argDict


dict2009 = read_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/2009Result.pkl')
dict2014 = read_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/2014Result.pkl')

'''
# lookup Plaka City is created and stored to constants.py file.
lookupPlakaCity = {}
for (plaka, city), party in dict2014.items():
    lookup_item = {plaka: city}
    lookupPlakaCity.update(lookup_item)

lookupPlakaCity = {a: toeng(b) for a, b in lookupPlakaCity.items()}
output = open('/home/cem/PycharmProjects/htmlParseInf/secim/PlakaCityMatch.pkl', 'wb')

pickle.dump(lookupPlakaCity, output)
'''

# update first letter of keys and replace start of party names unnecessary things of -
dict2009 = {a.capitalize(): b.replace('- ', '') for a, b in dict2009.items()}

lookup_Plaka_City_Inverse = {v: k for k, v in lookup_Plaka_City}

# party headerslerinin icindeki ilk itemler onlara ait semboller
headers = [AKP_HEADERS,
           MHP_HEADERS,
           DP_HEADERS,
           DSP_HEADERS,
           BAGIMSIZ_HEADERS,
           BDP_HEADERS,
           CHP_HEADERS,
           BBP_HEADERS,
           DTP_HEADERS]

dict2009 = getPartySymbol(argDict=dict2009, headers=headers)
dict2014 = getPartySymbol(argDict=dict2014, headers=headers)

import pandas as pd

d = {
    '2014': {
        '2014_Result': [v for k, v in dict2014.items()],
        'plaka': [k[0] for k, v in dict2014.items()],
        'city': [k[1] for k, v in dict2014.items()],
    },
    '2009': {
        '2009_Result': [v for k, v in dict2009.items()],
        'city': [k for k, v in dict2009.items()],
    }
}

df2014 = pd.DataFrame(data=d['2014'])
df2009 = pd.DataFrame(data=d['2009'])

df2014['city'] = [toeng(i) for i in df2014['city'].values]
dfSelection = df2014.join(df2009.set_index('city'), on='city')

# df = df.set_index(['plaka', 'city'])
dfSelection = dfSelection.sort_values(by=['plaka'])



df2009.to_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/df2009.pkl')
df2014.to_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/df2014.pkl')
dfSelection.to_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/dfSelection.pkl')


