
# Accessing the SCP York database
A quick demonstration on how to do this using the R PostgreSQL library
`install.packages('RPostgreSQL')`

PYTHON USAGE: Read NOTES.md , and import the load file: `from load import *`.  Here you can use `cursor.execute("<SELECT ... >")` to submit queries.

R can be installed on anaconda using `conda install -c r r-irkernel`


For questions contact daniel.ellis@york.ac.[uk]

```R
library('RPostgreSQL')
```

    Loading required package: DBI



```R
# Lets log into the database

pg = dbDriver("PostgreSQL")

cred = scan('~/.postgres_login', what="character")

con = dbConnect(pg, user= cred[1], password= cred[2],
                host= paste(cred[3],".york.ac.uk",sep=''),
                port=5432, dbname=cred[4])


```

### Now we are connected, we can have a look at querying.


## Reading a Table
Lets read the first 5 results from the countries table.

Double quotation marks are not usually needed.



```R
sql = 'SELECT * from "comm_trade.countries" LIMIT 5;'
```


```R
# read back the full table
dtab = dbGetQuery(con, sql)
```


```R
dtab
```


<table>
<thead><tr><th scope=col>index</th><th scope=col>area_code</th><th scope=col>name</th><th scope=col>iso</th></tr></thead>
<tbody>
	<tr><td>0         </td><td> 10       </td><td>Antarctica</td><td>ATA       </td></tr>
	<tr><td>1         </td><td>100       </td><td>Bulgaria  </td><td>BGR       </td></tr>
	<tr><td>2         </td><td>104       </td><td>Myanmar   </td><td>MMR       </td></tr>
	<tr><td>3         </td><td>108       </td><td>Burundi   </td><td>BDI       </td></tr>
	<tr><td>4         </td><td>112       </td><td>Belarus   </td><td>BLR       </td></tr>
</tbody>
</table>



### If we wish to only take the 'name' and 'area_code' columns:


```R
sql = '
        SELECT name,area_code
        from "comm_trade.countries"
        LIMIT 5;
'
# read back the full table
dtab = dbGetQuery(con, sql)
dtab
```


<table>
<thead><tr><th scope=col>name</th><th scope=col>area_code</th></tr></thead>
<tbody>
	<tr><td>Antarctica</td><td> 10       </td></tr>
	<tr><td>Bulgaria  </td><td>100       </td></tr>
	<tr><td>Myanmar   </td><td>104       </td></tr>
	<tr><td>Burundi   </td><td>108       </td></tr>
	<tr><td>Belarus   </td><td>112       </td></tr>
</tbody>
</table>



## Structure
Databases consist of groups of tables (Schemas). These represent the different projects that may exist

# List all schemas
Use `\dn+` in psql


```R
sql = 'SELECT schema_name
       FROM information_schema.schemata'
dbGetQuery(con, sql)

```


<table>
<thead><tr><th scope=col>schema_name</th></tr></thead>
<tbody>
	<tr><td>pg_catalog        </td></tr>
	<tr><td>information_schema</td></tr>
	<tr><td>public            </td></tr>
	<tr><td>scpdata           </td></tr>
	<tr><td>comm_trade        </td></tr>
	<tr><td>fao               </td></tr>
</tbody>
</table>



### If we then wish to see what tables exist within a certain schema (eg. fao)


```R
sql = "
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='fao';
"
dtab = dbGetQuery(con, sql)
dtab

```


<table>
<thead><tr><th scope=col>table_name</th></tr></thead>
<tbody>
	<tr><td>element      </td></tr>
	<tr><td>flags        </td></tr>
	<tr><td>countries    </td></tr>
	<tr><td>items        </td></tr>
	<tr><td>cb_production</td></tr>
</tbody>
</table>



### Finally we may also view the properties of a table within that schema, e.g. the commodity balance table from the fao schema

Use `\dt` tablename in psql


```R
sql = "
    SELECT table_catalog,table_schema,table_name,column_name,ordinal_position,is_nullable,data_type,character_maximum_length
    FROM information_schema.columns
    WHERE table_schema = 'fao' AND table_name = 'cb_production'
;"
dtab = dbGetQuery(con, sql)
dtab

```


<table>
<thead><tr><th scope=col>table_catalog</th><th scope=col>table_schema</th><th scope=col>table_name</th><th scope=col>column_name</th><th scope=col>ordinal_position</th><th scope=col>is_nullable</th><th scope=col>data_type</th><th scope=col>character_maximum_length</th></tr></thead>
<tbody>
	<tr><td>scpdata          </td><td>fao              </td><td>cb_production    </td><td>area_code        </td><td>1                </td><td>NO               </td><td>integer          </td><td> NA              </td></tr>
	<tr><td>scpdata          </td><td>fao              </td><td>cb_production    </td><td>item_code        </td><td>2                </td><td>NO               </td><td>integer          </td><td> NA              </td></tr>
	<tr><td>scpdata          </td><td>fao              </td><td>cb_production    </td><td>year             </td><td>3                </td><td>NO               </td><td>integer          </td><td> NA              </td></tr>
	<tr><td>scpdata          </td><td>fao              </td><td>cb_production    </td><td>unit             </td><td>4                </td><td>YES              </td><td>character varying</td><td>500              </td></tr>
	<tr><td>scpdata          </td><td>fao              </td><td>cb_production    </td><td>value            </td><td>5                </td><td>NO               </td><td>numeric          </td><td> NA              </td></tr>
	<tr><td>scpdata          </td><td>fao              </td><td>cb_production    </td><td>flag             </td><td>6                </td><td>YES              </td><td>character varying</td><td>  5              </td></tr>
</tbody>
</table>



# Querying
### Now lets explore the contents
(showing only the first 5 results)


```R
sql = 'SELECT * from fao.cb_production LIMIT 5;'
dtab = dbGetQuery(con, sql)
dtab
```


<table>
<thead><tr><th scope=col>area_code</th><th scope=col>item_code</th><th scope=col>year</th><th scope=col>unit</th><th scope=col>value</th><th scope=col>flag</th></tr></thead>
<tbody>
	<tr><td>2     </td><td>2617  </td><td>1961  </td><td>tonnes</td><td>15100 </td><td>S     </td></tr>
	<tr><td>2     </td><td>2617  </td><td>1962  </td><td>tonnes</td><td>15100 </td><td>S     </td></tr>
	<tr><td>2     </td><td>2617  </td><td>1963  </td><td>tonnes</td><td>15100 </td><td>S     </td></tr>
	<tr><td>2     </td><td>2617  </td><td>1964  </td><td>tonnes</td><td>18400 </td><td>S     </td></tr>
	<tr><td>2     </td><td>2617  </td><td>1965  </td><td>tonnes</td><td>20400 </td><td>S     </td></tr>
</tbody>
</table>



### What if we want only the values for year 2013


```R
sql = 'SELECT * from fao.cb_production WHERE year = 2013 LIMIT 5;'
dbGetQuery(con, sql)
```


<table>
<thead><tr><th scope=col>area_code</th><th scope=col>item_code</th><th scope=col>year</th><th scope=col>unit</th><th scope=col>value</th><th scope=col>flag</th></tr></thead>
<tbody>
	<tr><td>2     </td><td>2617  </td><td>2013  </td><td>tonnes</td><td> 78597</td><td>S     </td></tr>
	<tr><td>2     </td><td>2513  </td><td>2013  </td><td>tonnes</td><td>514000</td><td>S     </td></tr>
	<tr><td>2     </td><td>2600  </td><td>2013  </td><td>tonnes</td><td>441732</td><td>S     </td></tr>
	<tr><td>2     </td><td>2614  </td><td>2013  </td><td>tonnes</td><td>  3000</td><td>S     </td></tr>
	<tr><td>2     </td><td>2661  </td><td>2013  </td><td>tonnes</td><td> 13917</td><td>S     </td></tr>
</tbody>
</table>



## Asigning an alias in the query
We may wish to shorten the name of what we are querying to save typing later on. Here we give the commodity balance production table the name `p`.


```R
sql = '
    SELECT *
    FROM fao.cb_production p
    WHERE p.year = 2013
    LIMIT 5;'
dbGetQuery(con, sql)
```


<table>
<thead><tr><th scope=col>area_code</th><th scope=col>item_code</th><th scope=col>year</th><th scope=col>unit</th><th scope=col>value</th><th scope=col>flag</th></tr></thead>
<tbody>
	<tr><td>2     </td><td>2617  </td><td>2013  </td><td>tonnes</td><td> 78597</td><td>S     </td></tr>
	<tr><td>2     </td><td>2513  </td><td>2013  </td><td>tonnes</td><td>514000</td><td>S     </td></tr>
	<tr><td>2     </td><td>2600  </td><td>2013  </td><td>tonnes</td><td>441732</td><td>S     </td></tr>
	<tr><td>2     </td><td>2614  </td><td>2013  </td><td>tonnes</td><td>  3000</td><td>S     </td></tr>
	<tr><td>2     </td><td>2661  </td><td>2013  </td><td>tonnes</td><td> 13917</td><td>S     </td></tr>
</tbody>
</table>



## Link two tables
Sometimes we wish to combine two tables to produce an output. We can do this through one of the many possible join commands. Here we join our item table with the current one on the item_code columns (conveniently named the same in both tables) using `JOIN items i ON(p.item_code = i.item_code)`



```R
sql = '
    SELECT *
    FROM fao.cb_production p
    JOIN fao.items i ON(p.item_code = i.item_code)
    WHERE p.year=2013  
    LIMIT 10;'
dbGetQuery(con, sql)
```


<table>
<thead><tr><th scope=col>area_code</th><th scope=col>item_code</th><th scope=col>year</th><th scope=col>unit</th><th scope=col>value</th><th scope=col>flag</th><th scope=col>item_code</th><th scope=col>item</th></tr></thead>
<tbody>
	<tr><td>2                              </td><td>2617                           </td><td>2013                           </td><td>tonnes                         </td><td> 78597                         </td><td>S                              </td><td>2617                           </td><td>Apples and products            </td></tr>
	<tr><td>2                              </td><td>2513                           </td><td>2013                           </td><td>tonnes                         </td><td>514000                         </td><td>S                              </td><td>2513                           </td><td>Barley and products            </td></tr>
	<tr><td>2                              </td><td>2600                           </td><td>2013                           </td><td>tonnes                         </td><td>441732                         </td><td>S                              </td><td>2600                           </td><td>Brans                          </td></tr>
	<tr><td>2                              </td><td>2614                           </td><td>2013                           </td><td>tonnes                         </td><td>  3000                         </td><td>S                              </td><td>2614                           </td><td>Citrus, Other                  </td></tr>
	<tr><td>2                              </td><td>2661                           </td><td>2013                           </td><td>tonnes                         </td><td> 13917                         </td><td>S                              </td><td>2661                           </td><td>Cotton lint                    </td></tr>
	<tr><td>2                              </td><td>2559                           </td><td>2013                           </td><td>tonnes                         </td><td> 27412                         </td><td>S                              </td><td>2559                           </td><td>Cottonseed                     </td></tr>
	<tr><td>2                              </td><td>2594                           </td><td>2013                           </td><td>tonnes                         </td><td> 11769                         </td><td>S                              </td><td>2594                           </td><td>Cottonseed Cake                </td></tr>
	<tr><td>2                              </td><td>2575                           </td><td>2013                           </td><td>tonnes                         </td><td>  4707                         </td><td>S                              </td><td>2575                           </td><td>Cottonseed Oil                 </td></tr>
	<tr><td>2                              </td><td>2625                           </td><td>2013                           </td><td>tonnes                         </td><td>303788                         </td><td>S                              </td><td>2625                           </td><td>Fruits, Other                  </td></tr>
	<tr><td>2                              </td><td>2620                           </td><td>2013                           </td><td>tonnes                         </td><td>610570                         </td><td>S                              </td><td>2620                           </td><td>Grapes and products (excl wine)</td></tr>
</tbody>
</table>



## Unique (DISTINCT) values
If we dont want duplicates, we can always call upon the distinct selector.


```R
# Get all the years in the year column, and return a list with no duplicates
sql = 'SELECT DISTINCT year
       FROM fao.cb_production
       ORDER BY "year" DESC
       LIMIT 5
'
dbGetQuery(con, sql)


```


<table>
<thead><tr><th scope=col>year</th></tr></thead>
<tbody>
	<tr><td>2013</td></tr>
	<tr><td>2012</td></tr>
	<tr><td>2011</td></tr>
	<tr><td>2010</td></tr>
	<tr><td>2009</td></tr>
</tbody>
</table>




```R

```
