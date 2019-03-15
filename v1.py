import pandas as pd
from bs4 import BeautifulSoup
import re


def getIndex1(table):
    item = table.find_all('tr')
    itemv2 = item.find('div', class_='gwt-HTML multi-language-content content-tr')
    itemv3 = itemv2.text.replace('\n', '')


def getRowTextFromTable(table):
    rows = []
    items = table.find_all('div', class_='gwt-Label multi-language-content content-tr')
    for item in items:
        text = item.text.replace('\n', '')
        list = re.findall("\S+\s{0}", text)
        name = '-'.join(list)
        rows.append(name)
    return rows


def has_no_class(tag):
    return not tag.has_attr('class')


def getTableWithIndex(ind, html):
    if html:
        table = html.find_all('table')[ind]
        return table


def getWholeTables(html):
    if html:
        wholeTables = html.find_all(lambda tag: tag.name == 'table' and 'taxonomy-title-panel' not in tag[
            'class'] and 'financial-header-table' not in tag['class'])
    return wholeTables


def get_table_rows(table, *args):
    tbody = table.find('tbody')
    trows = tbody.findChildren('tr', recursive=False)
    cols = {}
    titles = {}
    footnotes = {}
    values = {}
    trowNumber = 0
    for trow in trows:
        if has_no_class(trow):
            cols[trowNumber] = trow
        elif trow['class'][0] == 'new-type-row':
            trowNumber += 1
            continue
            # continue
        else:
            tdatas = trow.find_all('td', recursive=False)
            for tdata in tdatas:
                if tdata.table:
                    if tdata['class'][0] == 'taxonomy-field-title':
                        text = tdata.text.replace('\n', '')
                        list = re.findall("\S+\s{0}", text)
                        name = '-'.join(list)
                        titles[trowNumber] = name
                if not has_no_class(tdata):
                    try:
                        if tdata['class'][0] == 'taxonomy-footnote-cell':
                            text = tdata.text.replace('\n', '')
                            list = re.findall("\S+\s{0}", text)
                            name = '-'.join(list)
                            footnotes[trowNumber] = name
                    except Exception as e:
                        print(str(e))
                    if tdata['class'][0] == 'taxonomy-context-value':
                        rr = re.compile('^col-order-class-[0-9]+$')
                        filtList = [m for item in tdata['class'] for m in [rr.search(item)] if m]
                        if len(filtList) > 0:
                            text = tdata.text.replace('\n', '')
                            list = re.findall("\S+\s{0}", text)
                            name = '-'.join(list)
                            if trowNumber in values:
                                values[trowNumber][filtList[0].string] = name
                            else:
                                values[trowNumber] = {filtList[0].string: name}

        trowNumber += 1

    return cols, titles, footnotes, values


# -------------------------------------- 2016 oncesi

