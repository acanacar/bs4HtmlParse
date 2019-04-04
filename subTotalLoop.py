import numpy as np
import math
from BilancoParse.constants import *
import pandas as pd


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


def doDiminish(x1, x2): return x1 - x2


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

    return datav2


def runSubTotalUnique(data, step):
    # sadece 1 tane step icin yapilacak subtotal.
    # coldiptoplam converting into float
    data['colDipToplam'] = data['colDipToplam'].astype(str).str.replace('.', '').astype(float)
    datav2 = data.copy()
    datav2 = flagDipToplam(data=datav2, step=step - 1)

    return datav2


def findZeroRows(data):
    dropRows = []
    for i, r in data.iterrows():
        if r['colDipToplam'] == 0:
            dropRows.append(i)
        if math.isnan(r['colDipToplam']):
            dropRows.append(i)
    return dropRows


def findMaxSubCount(data, maxStep):
    for j in range(maxStep, 0, -1):
        data_v = runSubTotalUnique(data=data, step=j)
        x = data_v.iloc[:, -1]
        a = sum([not bool(math.isnan(b)) for b in x])
        if a > 0:
            return j


def addRemoveDataFrame(data):
    dfList = []
    dropIndices = []
    colend = data.columns[-1]
    for i, r in data.iterrows():
        if math.isnan(r[colend]):
            continue
        else:
            intcolend = int(r[colend])
            d = data.loc[i + 1:i + 1 + intcolend, :]
            d['SubCode'] = str(r['tableindex']) + '.'
            dfList.append(d)
            l = list(range(i + 1, i + 1 + intcolend))
            dropIndices = dropIndices + l

    return dfList, dropIndices


def getMaxSubCount(data):
    maxSubCount = findMaxSubCount(data=data, maxStep=10)
    return maxSubCount


def runPart1(data):
    maxSubCount = findMaxSubCount(data=data, maxStep=15)
    # 3 maxsubcount demektirki 3 tane alt item toplami uste esit olan item mevcut.
    print('maxSubCount sona erdi. maxSubCount: ', maxSubCount)
    if maxSubCount > 0:
        df = data
        df = runSubTotalUnique(data=df, step=maxSubCount)
        # print('runSubTotalUnique sona erdi')
        dfList, dropIndices = addRemoveDataFrame(data=df)
        # print('addRemoveDataFrame sona erdi')
        df = df.drop(dropIndices)
        df.index = range(0, len(df))
        df = df.iloc[:, :-1]
        return df, dfList
    else:
        print('Process is completed')

def join2col(x):
    if type(x['SubCode']) == str:
        return int(x['SubCode'][:-1])
    else:
        return x['tableindex']

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
    lastdfOp = data
    while certainValue < 100:
        try:
            data, dfList = runPart1(data=data)
            lastdfOp = data
            mainDfList += dfList
        except Exception as e:
            print(str(e))
            break
        print('tur: ', certainValue)
        certainValue += 1

    Dfs = pd.concat(mainDfList)
    DatafN = pd.concat([Dfs, lastdfOp])
    DatafN = DatafN.dropna(how='all', axis='columns')

    DatafN = DatafN.sort_values(by=['tableindex'])
    DatafN.index = range(0, len(DatafN))

    return DatafN



def runPart2(data):
    maxSubCount = findMaxSubCount(data=data, maxStep=15)
    print('maxSubCount sona erdi. maxSubCount: ', maxSubCount)

    if maxSubCount:
        # maxSubCount_flag column is added
        data_w_flag = runSubTotalUnique(data=data, step=maxSubCount)
        indices = list(data_w_flag.index[data_w_flag[data_w_flag.columns[-1]].notnull()])
        dicLookup = {}
        for i in indices:
            val = data.loc[i, 'tableindex']
            keys = data.loc[i + 1:i + 10, 'tableIndexSubCodeJoin']
            dic = {key: val for key in keys}
            dicLookup.update(dic)

        data_wo_flag = data_w_flag.iloc[:, :-1].drop(indices)
        data_wo_flag.index = range(0, len(data_wo_flag))
        return dicLookup, data_wo_flag
    else:
        print('Process is completed')