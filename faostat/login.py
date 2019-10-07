#!/usr/bin/python

import psycopg2
import pandas as pd
from os.path import expanduser
import sys
home = expanduser("~")
cred = [i.strip() for i in tuple(open(home + '/.postgres_login'))]
conn = None

try:
    conn = psycopg2.connect(user = cred[0],
                                  password = cred[1],
                                  host = cred[2],
                                  port = "5432",
                                  database = cred[3])
    cursor = conn.cursor()
    # Print PostgreSQL Connection properties
    print ( conn.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
    sys.exit()



'''

if conn is not None:
        conn.close()

'''
