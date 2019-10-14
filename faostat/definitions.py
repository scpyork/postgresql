#!/usr/bin/python
'''
Create the 6nf style relatable item tables in Postgre


'''
from login import *
print (conn)

cursor.execute('CREATE SCHEMA IF NOT EXISTS fao;')


__loc__ = '/run/user/1000/gvfs/sftp:host=sftp.york.ac.uk,user=dp626/shared/storage/sei/SEI-Y RESEARCH GROUPS/SCP Group/SHARED RESOURCES/FAOSTAT_DATA/'
__loc__ = '../data/'


df = pd.read_csv(__loc__+'DEFINITIONS/countries.csv', dtype = str).astype(str)

c = [ u'Country Code', u'Country', u'M49 Code', u'ISO2 Code', u'ISO3 Code']




#remove duplicates
countries = df[c].groupby(by=[u'Country Code']).agg(lambda x: '|'.join(set(x.values[0].split('|'))))
countries.to_csv('temp.csv', index = True, header=False)

print('countries')
cmd = {
'countries':"""
                DROP TABLE IF EXISTS fao.countries;
                CREATE TABLE fao.countries (
                        country_code INTEGER PRIMARY KEY,
                        country VARCHAR(50) NOT NULL,
                        M49 VARCHAR(4),
                        ISO2 VARCHAR(4),
                        ISO3 VARCHAR(4)
                        );
            """,
}

for c in cmd:
    cursor.execute(cmd[c])
    print ('load')
    with open('./temp.csv', 'r') as f:
        #next(f) # Skip the header row.
        cursor.copy_expert(r"COPY fao.%s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        #cursor.copy_from(f, c, sep=',')
        conn.commit()



df = pd.read_csv(__loc__+'Food_Balance/Commodity_Balances/Crops_Primary_Equivalent.csv', dtype= str)


#### Item
it = df[[u'Item Code', u'Item']].groupby(by=[u'Item Code']).agg(lambda x: '|'.join(set(x.values[0].split('|'))))
it.to_csv('temp.csv', index = True, header=False)
print('item')
cmd = {

'items':"""
                DROP TABLE IF EXISTS fao.items;
                CREATE TABLE fao.items (
                        item_code INTEGER PRIMARY KEY,
                        item VARCHAR(50) NOT NULL
                        );
            """,
}

for c in cmd:
    cursor.execute(cmd[c])
    with open('./temp.csv', 'r') as f:

        cursor.copy_expert(r"COPY fao.%s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        conn.commit()




#### Element
ele = df[[u'Element Code', u'Element']].groupby(by=[u'Element Code']).agg(lambda x: '|'.join(set(x.values[0].split('|'))))
ele.to_csv('temp.csv', index = True, header=False)

print('element')

cmd = {

'element':"""
                DROP TABLE IF EXISTS fao.element;
                CREATE TABLE fao.element (
                        element_code INTEGER PRIMARY KEY,
                        element VARCHAR(50) NOT NULL
                        );
            """,
}

for c in cmd:
    cursor.execute(cmd[c])
    with open('./temp.csv', 'r') as f:

        cursor.copy_expert(r"COPY fao.%s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        conn.commit()



####Flags

cmd = {
'flags':"""
                DROP TABLE IF EXISTS fao.flags;
                CREATE TABLE fao.flags (
                        id INTEGER PRIMARY KEY,
                        flag VARCHAR(5),
                        desciption VARCHAR(250)
                        );
            """,
}

flag = pd.read_csv(__loc__+'DEFINITIONS/flags.csv')
#flag = flag.set_index('Flag')
flag.to_csv('temp.csv', index = True, header=False)

for c in cmd:
    cursor.execute(cmd[c])
    print ('load')
    import os
    #os.system('echo ls')
    #os.system('cp %s ./temp.csv'%(__loc__+'DEFINITIONS/flags.csv'))
    #os.system("sed '1d' ./temp.csv > ./temp.csv")
    with open('./temp.csv', 'r') as f:
        #next(f) # Skip the header row.
        cursor.copy_expert(r"COPY fao.%s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        #cursor.copy_from(f, c, sep=',')
        conn.commit()







'''
https://www.dataquest.io/blog/loading-data-into-postgres/
http://www.postgresqltutorial.com/
'''
