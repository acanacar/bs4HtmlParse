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
