import pandas as pd
import glob
from multiprocessing import Pool
from login import *

#Classification,Year,Period,Period Desc.,Aggregate Level,Is Leaf Code,Trade Flow Code,Trade Flow,Reporter Code,Reporter,Reporter ISO,Partner Code,Partner,Partner ISO,Commodity Code,Commodity,Qty Unit Code,Qty Unit,Qty,Netweight (kg),Trade Value (US$),Flag

files = list(filter( lambda x: 'corrected' in x, glob.glob('../../Comtrade_parse/data/*csv')))


def individual(f):

    import time
    start_time = time.time()
    d = pd.read_csv(f,dtype=str)
    print ('-- start',f)

    items = d[['Classification','Commodity Code','Commodity']]
    items = items.groupby(by=list(items.columns)).first().index
    items = pd.DataFrame(list(items))

    r = d['Reporter Code,Reporter,Reporter ISO'.split(',')]
    r = r.groupby(by=list(r.columns)).first().index
    r = pd.DataFrame(list(r))

    p = d['Partner Code,Partner,Partner ISO'.split(',')]
    p = p.groupby(by=list(p.columns)).first().index
    p = pd.DataFrame(list(p))

    countries = pd.concat([r,p], axis = 0)

    qty = d['Qty Unit Code,Qty Unit'.split(',')]
    qty = qty.groupby(by=list(qty.columns)).first().index
    qty = pd.DataFrame(list(qty))

    trade = d['Trade Flow Code,Trade Flow'.split(',')]
    trade = trade.groupby(by=list(trade.columns)).first().index
    trade = pd.DataFrame(list(trade))

    print("--- %s minutes to complete ---\n" % ((time.time() - start_time)/60.) , f, d.shape)
    return items, countries, qty, trade

'''
pool = Pool(processes=20)              # start 4 worker processes

data = pool.map(individual, files[:10])
g = []
print ('final')
for i,n in enumerate('items,countries,qty,trade'.split(',')):
    print(n)
    nd = pd.concat([j[i] for j in data],axis = 0, ignore_index = True)

    nd = nd.groupby(by=list(nd.columns)).first().index
    nd = pd.DataFrame(list(nd))
    import csv

    nd.to_csv(n+'.csv',index_label=False,index=False,# quotechar='"',
                      header=False)
'''
print('maketables')
cmd = {
'items':"""
                DROP TABLE IF EXISTS comm_trade.items;
                CREATE TABLE comm_trade.items (
                        classification VARCHAR(5) ,
                        commodity_code VARCHAR(10) ,
                        description VARCHAR(500),
                        PRIMARY KEY (classification,commodity_code)
                        );
            """,
'countries':"""
                DROP TABLE IF EXISTS comm_trade.countries;
                CREATE TABLE comm_trade.countries (
                        area_code INTEGER PRIMARY KEY,
                        name VARCHAR(500) ,
                        ISO VARCHAR(10)
                        );
            """,
'qty':"""
                DROP TABLE IF EXISTS comm_trade.qty;
                CREATE TABLE comm_trade.qty (
                        qty_code INTEGER PRIMARY KEY,
                        qty VARCHAR(100)
                        );
            """,
'trade':"""
                DROP TABLE IF EXISTS comm_trade.trade;
                CREATE TABLE comm_trade.trade (
                        trade_code INTEGER PRIMARY KEY,
                        trade VARCHAR(100)
                        );
            """,



}#//flag INTEGER REFERENCES flags(flag),

cursor.execute('CREATE SCHEMA IF NOT EXISTS comm_trade;')


for c in cmd:
    print ( c )
    cursor.execute(cmd[c])


from sqlalchemy import create_engine
#dialect+driver://username:password@host:port/database
engine = create_engine('postgresql://%s:%s@%s:5432/%s'%(cred[0],cred[1],cred[2]+'.york.ac.uk',cred[3]))

for i in 'items,countries,qty,trade'.split(','):
        print( 'final',i)
        import pandas.io.sql as sqlio
        table =  sqlio.read_sql_query('SELECT * FROM comm_trade.%s LIMIT 0;'%i, conn)

        df = pd.read_csv('%s.csv'%i)


        df.columns = table.columns
        df.to_sql('comm_trade.%s'%i, engine, if_exists='append', chunksize= 5000)





        '''
        with open('./%s.csv'%i, 'r') as f:
            #next(f) # Skip the header row.
            #
            cursor.copy_expert(r"COPY comm_trade.%s from stdin CSV QUOTE E'\"'  ENCODING 'LATIN1';"%c,f)
            #cursor.copy_from(f,'comm_trade.%s'%c, sep=',', null='\\N',  columns=None)
            conn.commit()
'''
