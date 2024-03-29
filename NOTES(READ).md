# PostgreSQL
Resources related to databasing

## Install
#### Python
```
sudo apt install postgresql-server-dev-all;
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org psycopg2
```
#### R
`install.packages('RPostgreSQL')`


## User login information

Under no circumstances do we wish to save our password in user scripts. The easiest way to avoid this by creating a hidden `.postgres_login` file containing all login credentials which we can read using another script. (Or you can use the config module if you know how to do that)


At `~/.postgres_login` (where tilde means your home directory) create the file.
This consists of 4 lines:

                                  user = cred[0],
                                  password = cred[1],
                                  host = cred[2],
                                  database = cred[3]

 and should be filled in the following manner:
 ```
 scpdata_read
 <mypass>
 pgscpdata
 scpdata
 ```

## Example login script
See faostat folder.

```python
import psycopg2
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
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)


 ```


## ADMIN CMDS - notes

- Show all schemas `select nspname from pg_catalog.pg_namespace;`



- Drop all tables `select 'drop table "' || tablename || '" cascade;' from pg_tables;`


`sudo -s ; su - postgres`
`createdb <name>`

```
GRANT { { CREATE | USAGE } [,...] | ALL [ PRIVILEGES ] }
    ON SCHEMA schema_name [, ...]
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]
 ```

```
#shell comands
createuser -PE demorole2
dropuser -i demorole2
createuser -sPE mysuperuser
```



## resource

https://launchschool.com/books/sql_first_edition/read/multi_tables
