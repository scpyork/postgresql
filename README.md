# PostgreSQL
Resources related to databasing

## Install
```
sudo apt install postgresql-server-dev-all;
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org psycopg2
```

## Add users 
`CREATE ROLE test WITH LOGIN ENCRYPTED PASSWORD 'test';` - new user named test
`\du` - see users 
`CREATE ROLE supertest WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD 'supertest'`
`\q` quit 

```
#shell comands 
createuser -PE demorole2
dropuser -i demorole2
createuser -sPE mysuperuser
```


## New db
1. Log in as user
