import psycopg2
import pandas as pd
import pandas.io.sql as sqlio

try:
    conn = psycopg2.connect(user = "admin",
                                  password = "admin",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "faostat")
    cursor = conn.cursor()
    # Print PostgreSQL Connection properties
    print ( conn.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)


def q(sql):
    import pandas.io.sql as sqlio
    return sqlio.read_sql_query(sql, conn)


sql = "select count(*) from trade_matrix;"
dat = sqlio.read_sql_query(sql, conn)

print (dat)

sql = '''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'trade_matrix';'''
dat = sqlio.read_sql_query(sql, conn)

print (dat)


#sql = '''SELECT DISTINCT "Reporter Countries", "Year" FROM trade_matrix;'''
#at = sqlio.read_sql_query(sql, conn)

#print (dat)

sql = '''SELECT DISTINCT "Item" FROM trade_matrix;'''
dat = sqlio.read_sql_query(sql, conn)

#print (dat)
for i in dat.values:
        if 'soy' in i[0].lower(): print i[0]

# q('select "Reporter Countries", "Year" FROM trade_matrix WHERE "Year" = 2003')

dat =  q('''SELECT "Reporter Countries","Partner Countries","Reporter Country Code","Partner Country Code","Element","Value"
FROM trade_matrix
WHERE "Year" = 2003 AND "Item" = 'Soybeans'
AND "Unit"='tonnes' AND "Value" > 0 AND "Reporter Country Code" < 500 AND "Partner Country Code" < 500
 ;''')

print dat

#conn = None
print ('fi')
