import sys

sys.path.append('/home/cem/PycharmProjects/htmlParseInf')
import pandas as pd
from bs4 import BeautifulSoup
from v2 import *
import requests

url = 'https://www.sabah.com.tr/gundem/2018/12/26/2014-yerel-secim-sonuclari-hangi-parti-hangi-ili-aldi'
response = requests.get(url)
html = BeautifulSoup(response.text, 'lxml')

if html:
    newBox = html.find('div', class_='newsDetailText')
    item_ul = newBox.find('ul')
    items_li = item_ul.find_all('li')

l = {}
for li in items_li:
    liText = li.text
    liText = liText.replace(' ', '')
    liText = liText.replace('–', '-')
    liText = liText.split('-')
    k, parti = liText[0], liText[1]
    plaka, il = k[:2], k[2:]
    l[(plaka, il)] = parti
