import pickle
from bs4 import BeautifulSoup
import requests
import time

pkl_file = open('/home/cem/PycharmProjects/htmlParseInf/secim/2014Result.pkl', 'rb')
myDict = pickle.load(pkl_file)
cities = [a[1] for a, b in myDict.items()]


def toeng(singleLine):
    choices = {"İ": "I", "ş": "s", "ç": "c", "Ç": "C", "ö": "o", "ü": "u", "ğ": "g", "ı": "i"}
    for i in range(len(singleLine)):
        singleLine = singleLine.replace(singleLine[i:i + 1], choices.get(singleLine[i], singleLine[i]))
    return singleLine


def getResults(html):
    resultsDiv = html.find('div', class_='ana-parti-listesi')
    firstPartyDiv = resultsDiv.find('div', class_='ana-parti-listesi-content')
    partyText = firstPartyDiv.find('span', class_='pa').text
    return partyText


myDict = {}
for city in cities:
    print(city, ' basladi')
    city = city.lower()
    city = toeng(city)
    url = 'https://secim.haberler.com/2009/{}-secim-sonuclari/'.format(city)
    response = requests.get(url, verify=False)
    myhtml = BeautifulSoup(response.text, 'lxml')
    if myhtml:
        try:
            result = getResults(myhtml)
            myDict[city] = result
        except Exception as e:
            print(str(e), city, '!!')
            continue
    else:
        print('there is no html for ', city)

import pickle

output = open('/home/cem/PycharmProjects/htmlParseInf/secim/2009Result.pkl', 'wb')

pickle.dump(myDict, output)
output.close()

print(myDict)
