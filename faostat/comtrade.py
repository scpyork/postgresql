import pandas as pd
from login import *

#__loc__ = r'/run/user/1000/gvfs/sftp:host=sftp.york.ac.uk,user=dp626/shared/storage/sei/SEI-Y RESEARCH GROUPS/SCP Group/SHARED RESOURCES/FAOSTAT_DATA/'


__loc__ = '../data/'

trade  = pd.read_csv(__loc__+'Detailed_trade_matrix.csv', dtype= str)

print('go')

trade = trade[trade['Reporter Country Code'].astype(int)<270 ]
trade = trade[trade['Partner Country Code'].astype(int)<270 ]
trade = trade[trade['Value'].astype(float)<0. ]

imports = trade[trade.Element == 'Import Quantity']
exports = trade[trade.Element == 'Export Quantity']

del trade

imports.columns = '~'.join(imports.columns).replace('Reporter Country Code','target').replace('Partner Country Code','source').split('~')

exports.columns = '~'.join(exports.columns).replace('Reporter Country Code','source').replace('Partner Country Code','target').split('~')


D = pd.concat([imports,exports],axis = 0, sort = True)

del imports,exports

cl = [u'Element Code', u'Flag', u'Item Code',
        u'Unit', u'Value', u'Year',
        u'source', u'target']

sql = """
                DROP TABLE IF EXISTS fao.trade_matrix;
                CREATE TABLE fao.trade_matrix (
                        id BIGINT PRIMARY KEY,
                        element_code INTEGER REFERENCES fao.element(element_code),
                        flag VARCHAR(5),
                        item integer REFERENCES fao.items(item_code),
                        unit VARCHAR(500),
                        value NUMERIC NOT NULL,
                        year INTEGER NOT NULL,
                        source INTEGER REFERENCES fao.countries(country_code),
                        target INTEGER REFERENCES fao.countries(country_code)
                        );
            """


D[cl].to_csv('temp.csv', index = True, header=False)

del D
print('to db')


cursor.execute(sql)
print ('load')
with open('./temp.csv', 'r') as f:
    #next(f) # Skip the header row.
    cursor.copy_expert(r"COPY fao.trade_matrix from stdin DELIMITERS ',' CSV QUOTE E'\"';",f)
    conn.commit()
