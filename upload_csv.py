'''
Add csv to postgres table (in faostat repo)

Arguments:
    1 - csv name
    2 - table name to give it in db
    3 - if exists: replace | append | fail

'''
import sys
import pandas as pd
df = pd.read_csv(sys.argv[1], encoding='latin-1')

try: exists = sys.argv[3]#append
except: exists = 'fail'

print df.dtypes

print ('read df')

from sqlalchemy import create_engine
engine = create_engine('postgresql://admin:admin@localhost:5432/faostat')


#cur.execute("DROP TABLE trade_matrix;")

df.to_sql(sys.argv[2], engine, if_exists=exists, chunksize= 5000)

print ('done')
