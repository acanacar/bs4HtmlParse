from v2 import *
import pandas as pd

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


def getDataFrameGelir(table):
    # read table
    dfs = pd.read_html(table.prettify(), header=0)
    df = dfs[0]
    cols = list(df.columns)
    print(len(cols))
    if len(cols) == 12:
        df = df.iloc[1:, [2, 6, 7, 8, 9, 10]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1], cols[2], cols[3], cols[4]
                    ]
        print('new_cols: ', new_cols)
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
        print('new_cols: ', new_cols)
        df.columns = new_cols
        df = df.dropna(axis=0, how='all')

        return df


bilancos = []
gelirs = []
nakits = []
k_bilancos = []
k_gelirs = []
k_nakits = []

year = 2017
mainDir = '/home/cem/PycharmProjects/htmlParseInf/Bilanco-zip/excels/2017/'
stock2 = ['ASELS']
for stock in stock2:
    a = time.time()
    print(stock, ' is started')
    readDir = mainDir + '{}_{}'.format(stock, year)

    if os.path.isdir(readDir):
        for file in os.listdir(readDir):

            if file.endswith(".html"):
                stock, file_no, year, donem = fileNameSplit(file)
                filepath = os.path.join(readDir, file)
                myhtml = BeautifulSoup(open(filepath))

                if myhtml:
                    konsolideText = getKonsolideFlag(myhtml)
                    if fromTexttoName(konsolideText) == 'Konsolide-Olmayan':
                        konsolide_f = 0
                    if fromTexttoName(konsolideText) == 'Konsolide':
                        konsolide_f = 1

                    myTables = getWholeTables(myhtml)
                    print(year, donem, konsolide_f, '#Tables -->', len(myTables))
                    headerAndTables = getHeaderandTable(Tables=myTables)

                    for header, table in headerAndTables.items():
                        if header in bilancoHeaders:
                            # print(header, '--> dfbilanco')
                            df = getDataFrameBilanco(table)
                            df['stock'] = stock
                            df['period'] = '{}_{}'.format(year, donem)
                            if konsolide_f == 1:
                                k_bilancos.append(df)
                            if konsolide_f == 0:
                                bilancos.append(df)

                        elif header in nakitAkisiHeaders:
                            # print(header, '--> dfnakit')
                            df = getDataFrameNakit(table)
                            df['stock'] = stock
                            df['period'] = '{}_{}'.format(year, donem)
                            if konsolide_f == 1:
                                k_nakits.append(df)
                            if konsolide_f == 0:
                                nakits.append(df)

                        elif header in karZararHeaders:
                            # print(header, '--> dfgelir')
                            df = getDataFrameGelir(table)
                            print('after operation: ', df.columns)
                            df['stock'] = stock
                            df['period'] = '{}_{}'.format(year, donem)
                            if konsolide_f == 1:
                                k_gelirs.append(df)
                            if konsolide_f == 0:
                                gelirs.append(df)

                        else:
                            print(header, ' hesaba katilmadi')
    b = time.time()
    print('lasted ', b - a)
