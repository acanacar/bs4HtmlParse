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
                    cols[1], cols[2]]
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
    if len(cols) == 9:
        df = df.iloc[1:, [2, 6, 7, 8]]
        new_cols = ['titles',
                    'footnotes',
                    cols[1], cols[2]]
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


url = '/home/cem/PycharmProjects/htmlParseInf/Bilanco-zip/excels/2017/AKBNK_2017/AKBNK_602678_2017_1.html'

myhtml = BeautifulSoup(open(url))
tabbles = getWholeTables(myhtml)
konsolideText = getKonsolideFlag(myhtml)

tab = tabbles[0]
ax = getHeaderandTable(tabbles)
headerTableList = list(ax.items())

tab_bil = headerTableList[0][1]
dfsBil = pd.read_html(tab_bil.prettify(), header=0)

tab_nakit = headerTableList[2][1]
dfsNak = pd.read_html(tab_nakit.prettify(), skiprows=2, header=0)

tab_gelir = headerTableList[3][1]
dfsGelir = pd.read_html(tab_nakit.prettify(), skiprows=2, header=0)

bilancos = []
karzarars = []
nakits = []

year = 2017
mainDir = '/home/cem/PycharmProjects/htmlParseInf/Bilanco-zip/excels/2017/'
for stock in Bist30Stocks:
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
                    headerAndTables = getHeaderandTable(Tables=myTables)

                    for header, table in headerAndTables.items():
                        if header in bilancoHeaders:
                            print(header)
                            df = getDataFrameBilanco(table)
                            bilancos.append(df)
                        if header in nakitAkisiHeaders:
                            print(header)
                            df = getDataFrameNakit(table)
                            nakits.append(df)

                        if header in karZararHeaders:
                            print(header)
                            df = getDataFrame(table)
                            karzarars.append(df)
