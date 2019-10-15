import pandas as pd
from py2neo import Graph,Node,Relationship,NodeMatcher

if str(raw_input('Type "wipe" to delete the entire network and reinitialise:\n'))=='wipe':

    graph =  Graph("http://localhost:7474/db/MRIO/",
     user="neo4j", password="sei")

    graph.delete_all()

    countries = pd.read_csv('data/countries.csv',keep_default_na=False)
    codes = pd.read_csv('data/countrycodes.csv',sep='\t',keep_default_na=False)


    for c in codes.iterrows():

        c=c[1]

        #if c['name'] == 'Namibia':c.aplha2='NA'

        latlon = countries[countries.Id==c.alpha2]

        if len(latlon >0):

            graph.create(Node("Country",
                alpha2=c.alpha2,
                alpha3=c.alpha3,
                numeric=c.numeric,
                name=c['name'],
                Lat=float(latlon.Lat.values[0]),
                Lon = float(latlon.Lon.values[0]),
                type='Country'))

        else:

            print 'no latlon',c
            graph.create(Node("Country",
                alpha2=c.alpha2,
                alpha3=c.alpha3,
                numeric=c.numeric,
                name=c['name'],
                type='Country'))


    for exio in 'ROM WWL WWE WWM WWA WWF'.split():
                    graph.create(Node("Country",
                        alpha3=exio,
                        exiobase=True,
                        type='Region',
                        name='Exiobase Region'))
