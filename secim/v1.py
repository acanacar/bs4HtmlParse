import pickle
from bs4 import BeautifulSoup
import requests
import urllib3


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


def read_pickle(path):
    pkl_file = open(path, 'rb')
    myDict = pickle.load(pkl_file)
    return myDict


def getHtml_doParse_doStore(cities):
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
    return myDict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# get cities of 2014 results dict
Dict2014 = read_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/2014Result.pkl')
cities = [a[1] for a, b in Dict2014.items()]

# get results of Dict 2009
Dict2009 = getHtml_doParse_doStore(cities=cities)


import pickle

output = open('/home/cem/PycharmProjects/htmlParseInf/secim/2009Result.pkl', 'wb')

pickle.dump(Dict2009, output)
output.close()

