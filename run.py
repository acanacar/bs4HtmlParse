from bs4 import BeautifulSoup
import pandas as pd

with open('Inf.html') as htmlfile:
    soup = BeautifulSoup(htmlfile, 'html.parser')

table = soup.find('table')
tablehead = table.find('thead')
tablebody = table.find('tbody')

rows = tablebody.find_all('tr')
columns = tablehead.find('tr').find_all('th')

col_names = [col.text for col in columns]
df_rows = [list(map(lambda x: x.text, row.find_all('td'))) for row in rows]

df = pd.DataFrame(columns=col_names, data=df_rows)
firstcolname, secondcolname, thirdcolname = df.columns
df.rename(columns={
    '{}'.format(firstcolname): 'date',
    '{}'.format(secondcolname): 'yearlyPercentageChange',
    '{}'.format(thirdcolname): 'monthlyPercentageChange',
}, inplace=True)
df = df.set_index('date')

df.to_csv('./Inf.csv', header=True, sep=',')
