import pandas as pd
from secim.constants import *

dfSelection = pd.read_pickle('/home/cem/PycharmProjects/htmlParseInf/secim/dfSelection.pkl')


def readTuikData(path):
    myDf = pd.read_csv(path, sep=';', header=0)
    myDf = myDf.transpose()

    myDf['cityEng'] = [toeng(i) for i in myDf.index.values]
    myDf = myDf.set_index('cityEng')
    return myDf


path = '/home/cem/PycharmProjects/htmlParseInf/secim/lib.csv'
dfLib = readTuikData(path=path)
pathGsyh = '/home/cem/PycharmProjects/htmlParseInf/secim/gsyh.csv'
dfGsyh = readTuikData(path=pathGsyh)

<<<<<<< HEAD
pathPopulation = '/home/cem/PycharmProjects/htmlParseInf/secim/nufus.csv'

dfPopulation = pd.read_csv(pathPopulation, sep=';', header=0)
dfPopulation = dfPopulation.pivot_table(values='population', index='city', columns='year')
dfPopulation['cityEng'] = [toeng(i) for i in dfPopulation.index.values]
dfPopulation = dfPopulation.set_index('cityEng')

df = dfSelection.join(dfLib, on='city')
df = df.set_index(['plaka', 'city'])
=======
df = dfSelection.join(dfLib, on='city')
df = df.set_index(['plaka', 'city'])


from bokeh.plotting import figure
from bokeh.io import show, output_notebook

# Create a blank figure with labels
p = figure(plot_width = 600, plot_height = 600, 
           title = 'Example Glyphs',
           x_axis_label = 'X', y_axis_label = 'Y')

# Example data
squares_x = [1, 3, 4, 5, 8]
squares_y = [8, 7, 3, 1, 10]
circles_x = [9, 12, 4, 3, 15]
circles_y = [8, 4, 11, 6, 10]

# Add squares glyph
p.square(squares_x, squares_y, size = 12, color = 'navy', alpha = 0.6)
# Add circle glyph
p.circle(circles_x, circles_y, size = 12, color = 'red')





>>>>>>> origin/master
