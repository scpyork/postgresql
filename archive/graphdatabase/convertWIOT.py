import pandas as pd
from py2neo import Graph,Node,Relationship,NodeMatcher
import os
graph =  Graph("http://localhost:7474/db/MRIO/",
     user="neo4j", password="sei")


'''convert xlsb to csv if needed, otherwise use the csv'''
filename = 'data/WIOT2014_Nov16_ROW.xlsb'
header = 2

if '.xlsb' in filename:
    csv = filename.replace('xlsb','csv')
    if os.path.exists(csv):
        filename = csv
        header = 0
    else:
        print('converting to csv')
        from pyxlsb import open_workbook
        with open(filename.replace('xlsb','csv'),'w') as f:
            with open_workbook(filename) as wb:
                #for sheetname in wb.sheets:
                    #with wb.get_sheet(sheetname) as sheet:
                        sheet = wb.get_sheet(wb.sheets[0])
                        for n,row in enumerate(sheet.rows()):
                            if n >= header:
                                values = [r.v for r in row]  # retrieving content

                                f.write(','.join((str(v) for v in values))+'\n')















print 'done'
