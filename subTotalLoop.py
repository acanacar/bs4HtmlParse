import numpy as np
import math
import pandas as pd


# def part2(data):
#     """ilk partta bulamadigimiz subcodelari bulmaya yarar.Burdan elde edilen resultLookup ile
#     main DataFrameimiz olan DfN dataframei SubCode columni guncellenir."""
#     resultLookups = {}
#     certainValue = 1
#     part2Dfs = []
#     dropIndices = []
#     while certainValue < 100:
#         try:
#             dicLookup, data_new, part2Df, Indice = runPart2(data=data)
#             print('dicLookup: ', dicLookup)
#             dropIndices.append(Indice)
#             part2Dfs.append(part2Df)
#             if len(data_new.columns) != len(data.columns):
#                 print(certainValue, ' icin column sayisinda artis olustu.: ', data_new.columns)
#
#             for k, v in dicLookup.items():
#                 data_new.loc[data_new['tableindex'] == k, 'SubCode'] = '{}.'.format(v)
#                 data_new.loc[data_new['tableindex'] == k, 'tableIndexSubCodeJoin'] = v
#             data = data_new
#             resultLookups.update(dicLookup)
#         except Exception as e:
#             print(str(e))
#             break
#         if certainValue % 25:
#             print('tur: ', certainValue)
#         certainValue += 1
#     return resultLookups, part2Dfs, dropIndices


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


def SubTotalForUniqueStep(data, step):
    # sadece 1 tane step icin yapilacak subtotal.
    # coldiptoplam converting into float
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
    maxSubCount = checkComponentAndGetItsStep(data=data, maxStep=20)
    # For instance if maxsubcount==3 means that there is component summed of 3 subitems.
    if maxSubCount:
        df = data
        try:
            df = SubTotalForUniqueStep(data=df, step=maxSubCount)
        except Exception as e:
            print('SubTotalForUniqueStep: ', str(e))
        # print('SubTotalForUniqueStep sona erdi')
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


def merge3col(x):
    S1 = 'SubCode1'
    S2 = 'SubCode2'
    S3 = 'SubCode3'
    try:
        if type(x[S1]) == str:
            return x[S1]
        elif type(x[S2]) == str:
            return x[S2]
        else:
            print(x[S3])
            return x[S3]
    except Exception as e:
        print(str(e), 'hata raised location row -> ', x)


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
        except Exception as e:
            print('Part1=>', str(e))
            break
        certainValue += 1

    Dfs = pd.concat(mainDfList)
    DatafN = pd.concat([Dfs, lastdfOps[-1]])
    DatafN = DatafN.dropna(how='all', axis='columns')

    DatafN = DatafN.sort_values(by=['tableindex'])
    DatafN.index = range(0, len(DatafN))

    return DatafN, mainDfList, lastdfOps


def checkComponentAndGetItsStep(data, maxStep):
    for j in range(maxStep, 0, -1):
        data_v = SubTotalForUniqueStep(data=data, step=j)
        x = data_v.iloc[:, -1]
        a = sum([not bool(math.isnan(b)) for b in x])
        if a > 0:
            return j


def findComponentPart(data):
    maxSubCount = checkComponentAndGetItsStep(data=data, maxStep=15)
    dicLookup = {}

    if maxSubCount:
        df = data
        # flag is added
        df = SubTotalForUniqueStep(data=df, step=maxSubCount)
        # WillComponentCreate indices
        indices = list(df.index[df[df.columns[-1]].notnull()])
        tableindices = list(df.tableindex[df[df.columns[-1]].notnull()])
        for i in indices:
            val = data.loc[i, 'tableindex']
            keys = data.loc[i + 1:i + maxSubCount, 'tableIndexSubCodeJoin']
            dic = {key: val for key in keys}
            dicLookup.update(dic)

    return dicLookup


def fillItemsOfComponent(data, lookup):
    for k, v in lookup.items():
        data.loc[data['tableindex'] == k, 'SubCode'] = '{}.'.format(v)
    return data


def FindOneItemComponentandItems(data):
    # component consisted of only one item
    s = data['SubCode'].value_counts()
    s = s[s == 1].index
    di = {}
    for item in s:
        val = data.loc[data['SubCode'] == item, 'tableindex'].values
        di.update({val[0]: int(item[:-1])})
    return di


def join2col(x):
    if type(x['SubCode']) == str:
        return int(x['SubCode'][:-1])
    else:
        return x['tableindex']


def getReadyPart2(data):
    # alt kalemleri bulunmus olanlarin table indexleri listesi
    foundKalems = set([int(i[:-1]) for i in data['SubCode'].values if type(i) == str])
    data1 = data.copy()
    oneItemComponentsLookup = FindOneItemComponentandItems(data1)
    '''bu partta yaptigim calismada alt kalemlerini bulamadiklarimizi her defasinda dataframeden cikaracagim.Bunu bir
    onceki parttaki calismada yapmadim.Cunku bu bulunamayan kalemleri tekrardan bulmak icin yaptigim bir calisma.'''
    data1 = data1.loc[~data1['tableindex'].isin(foundKalems)]
    data1['tableIndexSubCodeJoin'] = data1.apply(join2col, axis=1)
    data1['tableIndexSubCodeJoin'] = data1['tableIndexSubCodeJoin'].replace(oneItemComponentsLookup)
    data1 = data1.sort_values(by=['tableindex'])
    data1.index = range(0, len(data1))
    return data1


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


def running2(data):
    """ilk partta bulamadigimiz subcodelari bulmaya yarar.Burdan elde edilen resultLookup ile
    main DataFrameimiz olan DfN dataframei SubCode columni guncellenir."""
    changed = 0
    try:
        dataReady = getReadyPart2(data=data)
        resultLookup = findComponentPart(data=dataReady)
        checkedResultLookup = checkResultLookup(data=data, lookup=resultLookup)
        data = fillItemsOfComponent(data=data, lookup=checkedResultLookup)
        if bool(checkedResultLookup):
            changed = 1
    except Exception as e:
        print('running2 =>', str(e))
    return data, bool(changed)


def running3(data, SubCode2):
    DfN3 = data.iloc[::-1]
    # some controls might be added
    DfN3 = DfN3[DfN3['SubCode'].apply(lambda x: type(x) != str)]
    DfN3.index = range(0, len(DfN3))
    try:
        Dff, DfNlist, lastdfOps = Part1(data=DfN3)
        part3lookup = {k[0]: k[1] for k in Dff[['tableindex', 'SubCode']].values if type(k[1]) == str}
        if part3lookup:
            for k, v in part3lookup.items():
                checkDuplicateCode = data.loc[data['SubCode'] == v, 'tableindex'].values
                item = [i for i in checkDuplicateCode if i not in list(part3lookup.keys())]
                if len(checkDuplicateCode) > 0:
                    if len(checkDuplicateCode) == 1:
                        item = [i for i in checkDuplicateCode if i not in list(part3lookup.keys())]
                        if len(item) > 0:
                            v = '{}.'.format(checkDuplicateCode[0])

                sCode = data.loc[data['tableindex'] == k, 'SubCode'].values[0]
                if not type(sCode) == str:
                    data.loc[data['tableindex'] == k, 'SubCode'] = v
                    print('Degistirilen table index : {} with value of : {}'.format(k, v))

        SubCode3 = data[['tableindex', 'SubCode']]
    except Exception as e:
        print(str(e), 'Part1 error is raised1')
        SubCode3 = SubCode2
        SubCode3['SubCode'] = float('nan')


    return DfN3, SubCode3
