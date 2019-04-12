import numpy as np
import math
import pandas as pd

#'runpart2 part2 ve part words are removed and with aim of
# increasing code efficieny by decreasing lines are done by remove or rebulti to old functions'

def join2col(x):
    if type(x['SubCode']) == str:
        return int(x['SubCode'][:-1])
    else:
        return x['tableindex']


def renameCols(data):
    lokkup = {'03': '1', '06': '2', '09': '3', '12': '4'}
    newCols = []
    for col in data.columns:
        colv1 = col.replace('Bir Önceki Dönem', '')
        colv2 = colv1.replace('Cari Dönem', '')
        colv3 = colv2.replace('Önceki Dönem', '')
        colv4 = colv3.replace(' ', '')
        if colv4.startswith(('30', '31')):
            colv5 = colv4.replace('-', '.')
            collist = colv5.split('.')
            newCol = '{}-{}-{}'.format(collist[2], lokkup[collist[1]], collist[3])
        else:
            newCol = colv4
        newCols.append(newCol)

    data.columns = newCols
    return data


def createColDipToplam(data):
    for i, r in data.iterrows():
        try:
            periodRow = r['period']
            colToGet = '{}-{}-Toplam'.format(periodRow[:4], periodRow[-1:])
        except Exception as e:
            print(str(e), i)
            continue
        try:
            if r[colToGet]:
                data.loc[i, 'colDipToplam'] = r[colToGet]
            else:
                data.loc[i, 'colDipToplam'] = np.nan
        except Exception as e:
            print(str(e), i, '-')
    return data


def findZeroRows(data):
    dropRows = []
    for i, r in data.iterrows():
        if r['colDipToplam'] == 0:
            dropRows.append(i)
        if math.isnan(r['colDipToplam']):
            dropRows.append(i)
    return dropRows


def doDiminish(x1, x2): return x1 - x2


def my_reduce_w_range(func, seq, range):
    first = seq[0]
    if first == 0:
        return np.nan

    ind = 0
    while ind < len(seq[1:]):
        item = seq[1:][ind]
        # next item is greater than current item
        first = func(first, item)
        if first == 0:
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
    while i + step + 1 < len(data):
        a = my_reduce_w_range(doDiminish, data.loc[i:i + step + 1, 'colDipToplam'].values, step)
        if not (math.isnan(a)):
            data.at[i, [colName]] = a
        i += 1
        if i % 1000 == 0:
            print(i)
    return data


def runSubTotalUnique(data, step):
    # sadece 1 tane step icin yapilacak subtotal.
    # coldiptoplam converting into float
    datav2 = data.copy()
    datav2 = flagDipToplam(data=datav2, step=step)
    return datav2


def addRemoveDataFrame(data):
    dfList = []
    dropIndices = []
    colend = data.columns[-1]
    for i, r in data.iterrows():
        if math.isnan(r[colend]):
            continue
        else:
            intcolend = int(r[colend])
            d = data.loc[i + 1:i + intcolend, :]
            d['SubCode'] = str(r['tableindex']) + '.'
            dfList.append(d)
            l = list(range(i + 1, i + 1 + intcolend))
            dropIndices = dropIndices + l

    return dfList, dropIndices


def runPart1(data):
    maxSubCount = findComponent(data=data, maxStep=15)
    # 3 maxsubcount demektirki 3 tane alt item toplami uste esit olan item mevcut.
    # print('maxSubCount sona erdi. maxSubCount: ', maxSubCount)
    if maxSubCount:
        df = data
        try:
            df = runSubTotalUnique(data=df, step=maxSubCount)
        except Exception as e:
            print('runSubTotalUnique: ', str(e))
        # print('runSubTotalUnique sona erdi')
        dfList, dropIndices = addRemoveDataFrame(data=df)
        # print('addRemoveDataFrame sona erdi')
        df = df.drop(dropIndices)
        df.index = range(0, len(df))
        df = df.iloc[:, :-1]
        return df, dfList
    # else:
    #     print('Process is completed')


def getReadyPart1(data):
    data.index = range(0, len(data))
    data['colDipToplam'] = data['colDipToplam'].astype(str).str.replace('.', '').astype(float)
    zeroRowsIndices = findZeroRows(data)
    data = data.drop(zeroRowsIndices)
    data.index = range(0, len(data))
    return data


def Part1(data):
    certainValue = 1
    mainDfList = []
    lastdfOps = [data]
    while certainValue < 100:
        if certainValue % 25:
            print('tur: ', certainValue)
        try:
            data, dfList = runPart1(data=data)
            lastdfOps.append(data)
            mainDfList += dfList
            print(len(mainDfList))
        except Exception as e:
            print(str(e), 'lenmaindfList: ', len(mainDfList))
            break
        certainValue += 1

    Dfs = pd.concat(mainDfList)
    DatafN = pd.concat([Dfs, lastdfOps[-1]])
    DatafN = DatafN.dropna(how='all', axis='columns')

    DatafN = DatafN.sort_values(by=['tableindex'])
    DatafN.index = range(0, len(DatafN))

    return DatafN, mainDfList, lastdfOps


def runPart2(data):
    maxSubCount = findComponent(data=data, maxStep=15)
    # print('maxSubCount sona erdi. maxSubCount: ', maxSubCount)
    if maxSubCount:
        # maxSubCount_flag column is added
        data_w_flag = runSubTotalUnique(data=data, step=maxSubCount)
        # dip toplami olan indexler
        indices = list(data_w_flag.index[data_w_flag[data_w_flag.columns[-1]].notnull()])
        indicesx = list(data_w_flag.tableindex[data_w_flag[data_w_flag.columns[-1]].notnull()])
        dicLookup = {}
        for i in indices:
            val = data.loc[i, 'tableindex']
            # 238
            keys = data.loc[i + 1:i + maxSubCount, 'tableIndexSubCodeJoin']
            dic = {key: val for key in keys}
            dicLookup.update(dic)

        data_w_flag_ = data_w_flag.iloc[:, :].drop(indices)
        data_wo_flag = data_w_flag.iloc[:, :-1].drop(indices)

        data_wo_flag.index = range(0, len(data_wo_flag))
        data_w_flag_.index = range(0, len(data_w_flag_))
        return dicLookup, data_wo_flag, data_w_flag_, indices
    else:
        print('Process is completed')


def getReadyPart2(data):
    # alt kalemleri bulunmus olanlarin table indexleri listesi
    foundKalems = set([int(i[:-1]) for i in data['SubCode'].values if type(i) == str])
    data1 = data.copy()
    '''bu partta yaptigim calismada alt kalemlerini bulamadiklarimizi her defasinda dataframeden cikaracagim.Bunu bir
    onceki parttaki calismada yapmadim.Cunku bu bulunamayan kalemleri tekrardan bulmak icin yaptigim bir calisma.'''
    data1 = data1.loc[~data1['tableindex'].isin(foundKalems)]
    data1['tableIndexSubCodeJoin'] = data1.apply(join2col, axis=1)
    data1 = data1.sort_values(by=['tableindex'])
    data1.index = range(0, len(data1))
    return data1


def part2(data):
    """ilk partta bulamadigimiz subcodelari bulmaya yarar.Burdan elde edilen resultLookup ile
    main DataFrameimiz olan DfN dataframei SubCode columni guncellenir."""
    resultLookups = {}
    certainValue = 1
    part2Dfs = []
    dropIndices = []
    while certainValue < 100:
        try:
            dicLookup, data_new, part2Df, Indice = runPart2(data=data)
            print('dicLookup: ', dicLookup)
            dropIndices.append(Indice)
            part2Dfs.append(part2Df)
            if len(data_new.columns) != len(data.columns):
                print(certainValue, ' icin column sayisinda artis olustu.: ', data_new.columns)

            for k, v in dicLookup.items():
                data_new.loc[data_new['tableindex'] == k, 'SubCode'] = '{}.'.format(v)
                data_new.loc[data_new['tableindex'] == k, 'tableIndexSubCodeJoin'] = v
            data = data_new
            resultLookups.update(dicLookup)
        except Exception as e:
            print(str(e))
            break
        if certainValue % 25:
            print('tur: ', certainValue)
        certainValue += 1
    return resultLookups, part2Dfs, dropIndices


def findComponent(data, maxStep):
    for j in range(maxStep, 0, -1):
        data_v = runSubTotalUnique(data=data, step=j)
        x = data_v.iloc[:, -1]
        a = sum([not bool(math.isnan(b)) for b in x])
        if a > 0:
            return j


def findComponent(data):
    maxSubCount = findComponent(data=data, maxStep=15)

    dicLookup, data_new, part2Df, Indice = runPart2(data=data)
    if len(data_new.columns) != len(data.columns):
        print(' icin column sayisinda artis olustu.: ', data_new.columns)
    for k, v in dicLookup.items():
        data_new.loc[data_new['tableindex'] == k, 'SubCode'] = '{}.'.format(v)
        data_new.loc[data_new['tableindex'] == k, 'tableIndexSubCodeJoin'] = v

    return data_new, part2Df, dicLookup, Indice

def fillItemsOfComponent(data):
    """ilk partta bulamadigimiz subcodelari bulmaya yarar.Burdan elde edilen resultLookup ile
    main DataFrameimiz olan DfN dataframei SubCode columni guncellenir."""
    resultLookups = {}
    certainValue = 1
    part2Dfs = []
    dropIndices = []
    try:
        data = getReadyPart2(data=data)
        data_new, part2Df, dicLookup, Indice = findComponent(data=data)
        dropIndices.append(Indice)
        part2Dfs.append(part2Df)
        resultLookups.update(dicLookup)

    except Exception as e:
        print(str(e))
    return resultLookups, part2Dfs, dropIndices

def checkResultLookup(data, lookup):
    newLookup = lookup.copy()
    for k, v in lookup.items():
        subCode = data.loc[data['tableindex'] == k, 'SubCode'].values[0]
        if type(subCode) == str:
            newKey = int(subCode[:-1])
            if newKey in newLookup:
                del newLookup[k]
            else:
                del newLookup[k]
                newLookup.update({newKey: v})
    return newLookup
