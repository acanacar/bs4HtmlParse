import pandas as pd

periods = ['2018_1', '2018_2']
stocks = ['ASELS', 'PGSUS']
tablos = ['Bilanco', 'Gelir', 'Nakit']

l = []
for p in periods:
    for stock in stocks:
        for tablo in tablos:
            path = '/home/cem/PycharmProjects/htmlParseInf/BilancoParse/subPartTitle/{}-{}-{}.csv'.format(tablo, stock,
                                                                                                          p)
            df = pd.read_csv(path, sep=',')
            if sum([1 for c in df.columns if c.startswith('Bir Önc')]):
                cols = ['Unnamed: 0', 'titles', 'footnotes',
                        'Cari', 'Onceki', 'BirOnceki',
                        'stock', 'period', 'tableindex', 'x']
            elif sum([1 for c in df.columns if c.startswith('Cari Dönem 3 Aylık')]):
                cols = ['Unnamed: 0', 'titles', 'footnotes',
                        'Cari', 'Onceki', 'Cari_3Aylik', 'Onceki_3Aylik',
                        'stock', 'period', 'tableindex', 'x']
            else:
                cols = ['Unnamed: 0', 'titles', 'footnotes',
                        'Cari', 'Onceki',
                        'stock', 'period', 'tableindex', 'x']
            df.columns = cols
            l.append(df)

df = pd.concat(l, ignore_index=True, join='inner')
colsToUse = ['titles', 'stock', 'period', 'Cari', 'Onceki']
df = df[colsToUse]
df['Cari'] = df['Cari'].str.replace('.', '')
df['Onceki'] = df['Onceki'].str.replace('.', '')
df['Cari'] = pd.to_numeric(df['Cari'], errors='coerce')
df['Onceki'] = pd.to_numeric(df['Onceki'], errors='coerce')

# dataframe w\ MI
df.set_index(['stock', 'period', 'titles'], inplace=True)
df.sort_index(inplace=True)

df.loc[('ASELS', '2018_1', 'Dönem Karı (Zararı)'), ['Cari', 'Onceki']]

df.loc[('ASELS', '2018_2', 'Vergi İadeleri (Ödemeleri)'), ['Cari', 'Onceki']]

df.loc[('PGSUS', '2018_2', 'Vergi İadeleri (Ödemeleri)'), ['Cari', 'Onceki']]

df.loc[('ASELS', '2018_1', ['Vergi İadeleri (Ödemeleri)', 'Dönem Karı (Zararı)']), ['Cari', 'Onceki']]

df.loc[((slice(None)), '2018_1', ['Vergi İadeleri (Ödemeleri)', 'Dönem Karı (Zararı)']), ['Cari', 'Onceki']]

df.loc[((slice(None)), (slice(None)), ['Vergi İadeleri (Ödemeleri)', 'Dönem Karı (Zararı)']), ['Cari', 'Onceki']]

df.loc[((slice(None)), '2018_1', (slice(None))), ['Cari', 'Onceki']]

df.loc[((slice(None)), '2018_1', (slice(None))), ['Cari']]

a = df.loc[('ASELS', '2018_1', 'Dönem Karı (Zararı)'), ['Cari', 'Onceki']]
cari_value = a.values[0][0]
onceki_value = a.values[0][1]

a = df.loc[('ASELS', '2018_1', 'Dönem Karı (Zararı)'), ['Cari']]
value = a.values[0][0]
