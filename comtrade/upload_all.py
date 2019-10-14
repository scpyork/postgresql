import pandas as pd
import glob
from multiprocessing import Pool
from login import *

#Classification,Year,Period,Period Desc.,Aggregate Level,Is Leaf Code,Trade Flow Code,Trade Flow,Reporter Code,Reporter,Reporter ISO,Partner Code,Partner,Partner ISO,Commodity Code,Commodity,Qty Unit Code,Qty Unit,Qty,Netweight (kg),Trade Value (US$),Flag

col = 'Classification,Year,Trade Flow Code,Reporter Code,Partner Code,Commodity Code,Qty Unit Code,Netweight (kg),Trade Value (US$),Flag'.split(',')

files = list(filter( lambda x: 'corrected' in x, glob.glob('../../Comtrade_parse/data/*csv')))
files.sort()

print( len(files) )

sql  = """
                DROP TABLE IF EXISTS comm_trade.data;
                CREATE TABLE comm_trade.data (
                        id INTEGER PRIMARY KEY,
                        classification VARCHAR(5),
                        year INTEGER NOT NULL,
                        trade_code INTEGER REFERENCES comm_trade.trade(trade_code),
                        reporter INTEGER REFERENCES comm_trade.countries(area_code),
                        partner INTEGER REFERENCES comm_trade.countries(area_code),
                        commodity_code VARCHAR(10) NOT NULL,
                        qty_code INTEGER REFERENCES comm_trade.qty(qty_code),
                        netweight INTEGER,
                        value INTEGER,
                        flag VARCHAR(10)
                        );

            """

sql  = """
                DROP TABLE IF EXISTS comm_trade.data;
                CREATE TABLE comm_trade.data (
                        id INTEGER PRIMARY KEY,
                        classification VARCHAR(5),
                        year INTEGER NOT NULL,
                        trade_code INTEGER ,
                        reporter INTEGER ,
                        partner INTEGER,
                        commodity_code VARCHAR(10) NOT NULL,
                        qty_code INTEGER,
                        netweight BIGINT,
                        value BIGINT,
                        flag VARCHAR(10)
                        );

            """



cursor.execute('CREATE SCHEMA IF NOT EXISTS comm_trade;')
cursor.execute(sql)


print('login')
from sqlalchemy import create_engine
#dialect+driver://username:password@host:port/database
engine = create_engine('postgresql://%s:%s@%s:5432/%s'%(cred[0],cred[1],cred[2]+'.york.ac.uk',cred[3]))

#SELECT * FROM "comm_trade.items" WHERE "commodity_code" = '0103' LIMIT 10
import pandas.io.sql as sqlio
table =  sqlio.read_sql_query('SELECT * FROM comm_trade.data LIMIT 0;', conn)
index = 0
for i in files:
        print (i)

        df = pd.read_csv('%s'%i,dtype=str)[col]
        df.columns = table.columns[1:]
        index+=1
        df.index = list(range(index,index+len(df)))
        df.to_csv('temp.csv', index = True, header=False)
        index += len(df)
        print ('add')
        with open('./temp.csv', 'r') as f:
            #next(f) # Skip the header row.
            cursor.copy_expert(r"COPY comm_trade.data from stdin DELIMITERS ',' CSV QUOTE E'\"';",f)
            conn.commit()




        #df.to_sql('comm_trade.data', engine, if_exists='append', chunksize= 5000)
