import pandas as pd
import numpy as np
import math
import re

def doDiminish(x1, x2): return x1 - x2


def renameCols(data):
    lokkup = {'03': '1', '06': '2', '09': '3', '12': '4'}
    newCols = []
    for col in df.columns:
        if col.startswith(('30', '31')):
            colv1 = col.replace('-', '.')
            collist = colv1.split('.')
            newCol = '{}-{}-{}'.format(collist[2], lokkup[collist[1]], collist[3])
        else:
            newCol = col
        newCols.append(newCol)
    data.columns = newCols
    return data

def my_reduce(func, seq):
    first = seq[0]
    if first == 0:
        return np.nan

    ind = 0
    while ind < len(seq[1:]):
        item = seq[1:][ind]
        # next item is greater than current item
        if first < item:
            return np.nan
        else:
            first = func(first, item)
            if first < 0:
                return np.nan
            if first == 0:
                print('first: ', first)
                print('item: ', item)
                return ind + 1
        ind += 1
    return np.nan


def my_reduce_w_range(func, seq, range):
    first = seq[0]
    if first == 0:
        return np.nan

    ind = 0
    while ind < len(seq[1:]):
        item = seq[1:][ind]
        # next item is greater than current item
        if first < item:
            return np.nan
        else:
            first = func(first, item)
            if first < 0:
                return np.nan
            if first == 0:
                print('first: ', first, 'item: ', item)
                if ind + 1 == range:
                    return ind + 1
                else:
                    try:
                        itemnext = seq[1:][ind + 1]
                        if itemnext == 0:
                            ind += 1
                            continue
                    except Exception as e:
                        print(str(e))
                        return np.nan
        ind += 1
    return np.nan


def flagDipToplam(data, step):
    colName = '{}_range_F'.format(step)
    data[colName] = np.nan
    i = 0
    while i < len(data):
        a = my_reduce_w_range(doDiminish, data.loc[i:i + step + 1, 'colDipToplam'].values, step)
        if not (math.isnan(a)):
            print(i)
            data.at[i, [colName]] = a
        i += 1
        if i % 1000 == 0:
            print(i)
    return data


def runSubTotal(data, maxstep):
    # coldiptoplam converting into float
    data['colDipToplam'] = data['colDipToplam'].astype(str).str.replace('.', '').astype(float)
    datav2 = data.copy()
    for i in range(1, maxstep):
        print(i)
        datav2 = flagDipToplam(data=datav2, step=i)
        print(i, 'sona erdi')

    data['max'] = datav2.iloc[:, -(maxstep - 1):].max(axis=1)
    datav2['max'] = data['max']
    return data, datav2
''' 2017 PARSING !!!! '''


def fileNameSplit(file):
    splittedFile = file[:-5].split('_')
    return splittedFile[0], splittedFile[1], splittedFile[2], splittedFile[3]


def get_table_titles_2017(table, *args):
    tbody = table.find('tbody')
    trows = tbody.findChildren('tr', recursive=False)
    titles = {}
    trowNumber = 0

    for trow in trows:
        if has_no_class(trow):
            continue
        elif trow['class'][0] == 'new-type-row':
            continue
        else:
            tdatas = trow.find_all('td', recursive=False)
            for tdata in tdatas:
                if tdata.table:
                    if tdata['class'][0] == 'taxonomy-field-title':
                        text = tdata.text.replace('\n', '')
                        list = re.findall("\S+\s{0}", text)
                        name = '-'.join(list)
                        titles[trowNumber] = name

        trowNumber += 1

    return titles


def getHeaderandTable(Tables):
    a = {}
    for index, table in enumerate(Tables):
        headers = get_table_titles_2017(table)
        headersList = [[k, v] for k, v in headers.items()]
        header = headersList[0][1]
        a[header] = table
    return a


def getDataFrameNakit(table):
    # read table
    dfs = pd.read_html(table.prettify(), header=0)
    df = dfs[0]
    cols = list(df.columns)
    if len(cols) == 9:
        df = df.iloc[1:, [2, 6, 7, 8]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1], cols[2]]
        df.columns = new_cols
        # drop rows with all nan
        df = df.dropna(axis=0, how='all')
        return df
    else:
        print('len(cols) 9 degil --> ', len(cols))


def getDataFrameBilanco(table):
    # read table
    dfs = pd.read_html(table.prettify(), header=0)
    df = dfs[0]
    cols = list(df.columns)
    if len(cols) == 9:
        df = df.iloc[1:, [2, 6, 7, 8]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1] + '-Toplam', cols[2] + '-Toplam']
        # replace old cari donem col name with titles
        df.columns = new_cols
        # drop rows with all nan
        df = df.dropna(axis=0, how='all')
        return df
    if len(cols) == 13:
        df = df.iloc[1:, [2, 6, 7, 8, 9, 10, 11, 12]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1] + '-YP', cols[1] + '-TP', cols[1] + '-Toplam',
                    cols[2] + '-YP', cols[2] + '-TP', cols[2] + '-Toplam']
        df.columns = new_cols
        df = df.dropna(axis=0, how='all')

        return df
    if len(cols) == 10:
        df = df.iloc[1:, [2, 6, 7, 8, 9]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1] + '-Toplam', cols[2] + '-Toplam', cols[3] + '-Toplam']
        df.columns = new_cols
        df = df.dropna(axis=0, how='all')

        return df

    else:
        print(len(cols), ' bulunamadi')


def getDataFrameGelir(table):
    # read table
    dfs = pd.read_html(table.prettify(), header=0)
    df = dfs[0]
    cols = list(df.columns)
    if len(cols) == 12:
        df = df.iloc[1:, [2, 6, 7, 8, 9, 10]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1], cols[2], cols[3], cols[4]
                    ]
        # replace old cari donem col name with titles
        df.columns = new_cols
        # drop rows with all nan
        df = df.dropna(axis=0, how='all')
        return df
    if len(cols) == 10:
        df = df.iloc[1:, [2, 6, 7, 8]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1], cols[2]
                    ]
        df.columns = new_cols
        df = df.dropna(axis=0, how='all')

        return df

def getKonsolideFlagForOld(html):
    if html:
        wholeTables = html.find_all(
            lambda tag: tag.name == 'table' and 'tablob' in tag['class'] if tag.has_attr('class') else False)
        konsolideText = wholeTables[0].find_all('tr')[1].find_all('td')[-1].text
    return konsolideText
def getKonsolideFlag(html):
    if html:
        wholeTables = html.find_all(lambda tag: tag.name == 'table' and 'financial-header-table' in tag['class'])
        konsolideText = wholeTables[0].find_all('td')[-1].text
    return konsolideText


def fromTexttoName(dataText):
    text = dataText.replace('\n', '')
    list = re.findall("\S+\s{0}", text)
    result = '-'.join(list)
    return result

def getConsolidateFlag(html, old_f):
    if old_f:
        konsolideText = fromTexttoName(getKonsolideFlagForOld(html))
    else:
        konsolideText = fromTexttoName(getKonsolideFlag(html))
    if konsolideText == 'Konsolide-Olmayan':
        return 0
    if konsolideText == 'Konsolide':
        return 1



def storeFrame2018(inputlist, outputname, outputpath):
    dataframe = pd.concat(inputlist)
    dataframe.to_pickle('{}/{}.pkl'.format(outputpath, outputname))
    dataframe.to_excel('/home/cem/Desktop/{}.xls'.format(outputname))


