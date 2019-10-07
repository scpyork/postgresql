#!/usr/bin/python
'''
Create the 6nf style relatable item tables in Postgre


'''
from login import *
print (conn)


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
                DROP TABLE IF EXISTS countries;
                CREATE TABLE countries (
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
    print 'load'
    with open('./temp.csv', 'r') as f:
        #next(f) # Skip the header row.
        cursor.copy_expert(r"COPY %s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        #cursor.copy_from(f, c, sep=',')
        conn.commit()



df = pd.read_csv(__loc__+'Food_Balance/Commodity_Balances/Crops_Primary_Equivalent.csv', dtype= str)


#### Item
it = df[[u'Item Code', u'Item']].groupby(by=[u'Item Code']).agg(lambda x: '|'.join(set(x.values[0].split('|'))))
it.to_csv('temp.csv', index = True, header=False)
print('item')
cmd = {

'items':"""
                DROP TABLE IF EXISTS items;
                CREATE TABLE items (
                        item_code INTEGER PRIMARY KEY,
                        item VARCHAR(50) NOT NULL
                        );
            """,
}

for c in cmd:
    cursor.execute(cmd[c])
    with open('./temp.csv', 'r') as f:

        cursor.copy_expert(r"COPY %s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        conn.commit()




#### Element
ele = df[[u'Element Code', u'Element']].groupby(by=[u'Element Code']).agg(lambda x: '|'.join(set(x.values[0].split('|'))))
ele.to_csv('temp.csv', index = True, header=False)

print('element')

cmd = {

'element':"""
                DROP TABLE IF EXISTS element;
                CREATE TABLE element (
                        element_code INTEGER PRIMARY KEY,
                        element VARCHAR(50) NOT NULL
                        );
            """,
}

for c in cmd:
    cursor.execute(cmd[c])
    with open('./temp.csv', 'r') as f:

        cursor.copy_expert(r"COPY %s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        conn.commit()



####Flags

cmd = {
'flags':"""
                DROP TABLE IF EXISTS flags;
                CREATE TABLE flags (
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
        cursor.copy_expert(r"COPY %s from stdin DELIMITERS ',' CSV QUOTE E'\"';"%c,f)
        #cursor.copy_from(f, c, sep=',')
        conn.commit()







'''
https://www.dataquest.io/blog/loading-data-into-postgres/
http://www.postgresqltutorial.com/


-- Assuming you have already created an imported_users table
-- Assuming your CSV has no headers
\copy imported_users from 'imported_users.csv' csv;

-- If your CSV does have headers, they need to match the columns in your table
\copy imported_users from 'imported_users.csv' csv header;

-- If you want to only import certain columns
\copy imported_users (id, email) from 'imported_users.csv' csv header;
'''




##############
#old
#####################

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
'''    for command in commands:
            cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()

'''
