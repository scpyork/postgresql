
from login import *

#__loc__ = r'/run/user/1000/gvfs/sftp:host=sftp.york.ac.uk,user=dp626/shared/storage/sei/SEI-Y RESEARCH GROUPS/SCP Group/SHARED RESOURCES/FAOSTAT_DATA/'
__loc__ = '../data/'

df = pd.read_csv(__loc__+'Food_Balance/Commodity_Balances/Crops_Primary_Equivalent.csv', dtype= str)

c  = [u'Area Code', u'Item Code',  u'Element Code', u'Year', u'Unit', u'Value', u'Flag']

prod = df[df.Element=='Production']
prod = prod[[u'Area Code', u'Item Code', u'Year', u'Unit', u'Value','Flag']]# u'Flag']]
prod = prod[prod['Area Code'].astype(int)<270 ]

#prod = prod.groupby(by=[u'Area Code','Item Code','Year']).sum()
prod.to_csv('temp.csv', index = False, header=False)

print('to db')

cmd = {

'cb_production':"""
                DROP TABLE IF EXISTS cb_production;
                CREATE TABLE cb_production (
                        area_code INTEGER REFERENCES countries(country_code),
                        item_code INTEGER REFERENCES items(item_code),
                        year INTEGER NOT NULL,
                        unit VARCHAR(500),
                        value NUMERIC NOT NULL,
                        flag VARCHAR(5),
                        PRIMARY KEY (area_code,item_code,year)
                        );
            """,
}#//flag INTEGER REFERENCES flags(flag),

for c in cmd:
    cursor.execute(cmd[c])
    print ('load')
    with open('./temp.csv', 'r') as f:
        #next(f) # Skip the header row.
        cursor.copy_expert(r"COPY %s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        conn.commit()
