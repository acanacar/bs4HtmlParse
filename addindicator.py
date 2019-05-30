import talib


def add_indicator(data):
    open = data.Open
    high = data.High
    low = data.Low
    close = data.Close
    volume = data.Volume

    data['CDL2CROWS'] = talib.CDL2CROWS(open, high, low, close)
    data['CDL3BLACKCROWS'] = talib.CDL3BLACKCROWS(open, high, low, close)
    data['CDL3INSIDE'] = talib.CDL3INSIDE(open, high, low, close)
    data['CDL3LINESTRIKE'] = talib.CDL3LINESTRIKE(open, high, low, close)
    data['CDL3OUTSIDE'] = talib.CDL3OUTSIDE(open, high, low, close)
    data['CDL3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(open, high, low, close)
    data['CDL3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(open, high, low, close)
    data['CDLABANDONEDBABY'] = talib.CDLABANDONEDBABY(open, high, low, close, penetration=0)

    data['CDLADVANCEBLOCK'] = talib.CDLADVANCEBLOCK(open, high, low, close)
    data['CDLBELTHOLD'] = talib.CDLBELTHOLD(open, high, low, close)
    data['CDLBREAKAWAY'] = talib.CDLBREAKAWAY(open, high, low, close)
    data['CDLCLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(open, high, low, close)
    data['CDLCONCEALBABYSWALL'] = talib.CDLCONCEALBABYSWALL(open, high, low, close)
    data['CDLCOUNTERATTACK'] = talib.CDLCOUNTERATTACK(open, high, low, close)
    data['CDLDARKCLOUDCOVER'] = talib.CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)

    data['CDLDOJI'] = talib.CDLDOJI(open, high, low, close)
    data['CDLDOJISTAR'] = talib.CDLDOJISTAR(open, high, low, close)
    data['CDLDRAGONFLYDOJI'] = talib.CDLDRAGONFLYDOJI(open, high, low, close)
    data['CDLENGULFING'] = talib.CDLENGULFING(open, high, low, close)
    data['CDLEVENINGDOJISTAR'] = talib.CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)

    data['CDLEVENINGSTAR'] = talib.CDLEVENINGSTAR(open, high, low, close, penetration=0)

    data['CDLGAPSIDESIDEWHITE'] = talib.CDLGAPSIDESIDEWHITE(open, high, low, close)
    data['CDLGRAVESTONEDOJI'] = talib.CDLGRAVESTONEDOJI(open, high, low, close)
    data['CDLHAMMER'] = talib.CDLHAMMER(open, high, low, close)
    data['CDLHANGINGMAN'] = talib.CDLHANGINGMAN(open, high, low, close)
    data['CDLHARAMI'] = talib.CDLHARAMI(open, high, low, close)
    data['CDLHARAMICROSS'] = talib.CDLHARAMICROSS(open, high, low, close)
    data['CDLHIGHWAVE'] = talib.CDLHIGHWAVE(open, high, low, close)
    data['CDLHIKKAKE'] = talib.CDLHIKKAKE(open, high, low, close)
    data['CDLHIKKAKEMOD'] = talib.CDLHIKKAKEMOD(open, high, low, close)
    data['CDLHOMINGPIGEON'] = talib.CDLHOMINGPIGEON(open, high, low, close)
    data['CDLIDENTICAL3CROWS'] = talib.CDLIDENTICAL3CROWS(open, high, low, close)
    data['CDLINNECK'] = talib.CDLINNECK(open, high, low, close)
    data['CDLINVERTEDHAMMER'] = talib.CDLINVERTEDHAMMER(open, high, low, close)
    data['CDLKICKING'] = talib.CDLKICKING(open, high, low, close)
    data['CDLKICKINGBYLENGTH'] = talib.CDLKICKINGBYLENGTH(open, high, low, close)
    data['CDLLADDERBOTTOM'] = talib.CDLLADDERBOTTOM(open, high, low, close)
    data['CDLLONGLEGGEDDOJI'] = talib.CDLLONGLEGGEDDOJI(open, high, low, close)
    data['CDLLONGLINE'] = talib.CDLLONGLINE(open, high, low, close)
    data['CDLMARUBOZU'] = talib.CDLMARUBOZU(open, high, low, close)
    data['CDLMATCHINGLOW'] = talib.CDLMATCHINGLOW(open, high, low, close)
    data['CDLMATHOLD'] = talib.CDLMATHOLD(open, high, low, close, penetration=0)

    data['CDLMORNINGDOJISTAR'] = talib.CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)

    data['CDLMORNINGSTAR'] = talib.CDLMORNINGSTAR(open, high, low, close, penetration=0)

    data['CDLONNECK'] = talib.CDLONNECK(open, high, low, close)
    data['CDLPIERCING'] = talib.CDLPIERCING(open, high, low, close)
    data['CDLRICKSHAWMAN'] = talib.CDLRICKSHAWMAN(open, high, low, close)
    data['CDLRISEFALL3METHODS'] = talib.CDLRISEFALL3METHODS(open, high, low, close)
    data['CDLSEPARATINGLINES'] = talib.CDLSEPARATINGLINES(open, high, low, close)
    data['CDLSHOOTINGSTAR'] = talib.CDLSHOOTINGSTAR(open, high, low, close)
    data['CDLSHORTLINE'] = talib.CDLSHORTLINE(open, high, low, close)
    data['CDLSPINNINGTOP'] = talib.CDLSPINNINGTOP(open, high, low, close)
    data['CDLSTALLEDPATTERN'] = talib.CDLSTALLEDPATTERN(open, high, low, close)
    data['CDLSTICKSANDWICH'] = talib.CDLSTICKSANDWICH(open, high, low, close)
    data['CDLTAKURI'] = talib.CDLTAKURI(open, high, low, close)
    data['CDLTASUKIGAP'] = talib.CDLTASUKIGAP(open, high, low, close)
    data['CDLTHRUSTING'] = talib.CDLTHRUSTING(open, high, low, close)
    data['CDLTRISTAR'] = talib.CDLTRISTAR(open, high, low, close)
    data['CDLUNIQUE3RIVER'] = talib.CDLUNIQUE3RIVER(open, high, low, close)
    data['CDLUPSIDEGAP2CROWS'] = talib.CDLUPSIDEGAP2CROWS(open, high, low, close)
    data['CDLXSIDEGAP3METHODS'] = talib.CDLXSIDEGAP3METHODS(open, high, low, close)
    #   data['ADX'] = talib.ADX(high, low, close, timeperiod=14)

    data['MACDFAS'], data['MACDSLO'], data['MACDSIGNA'] = talib.MACD(close, fastperiod=12, slowperiod=26,
                                                                     signalperiod=9)
    data['3day MA'] = close.shift(1).rolling(window=3).mean()
    data['10day MA'] = close.shift(1).rolling(window=10).mean()
    data['30day MA'] = close.shift(1).rolling(window=30).mean()
    data['RSI_9'] = talib.RSI(close.values, timeperiod=9)
    data['S_10'] = close.rolling(window=10).mean()
    data['Corr'] = close.rolling(window=10).corr(data['S_10'])
    data['Williams %R'] = talib.WILLR(data['High'].values, data['Low'].values, data[
        'Close'].values, 7)

    return data
