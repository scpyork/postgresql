import pandas as pd
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import numpy as np
import json
import scipy.sparse as sp


graph =  Graph("http://localhost:7474/db/MRIO/",user="neo4j", password="sei")



'''add a check if this file has been parsed'''
__location__ = 'data/exiobase/'
for year in range(2005,2012):

    dir = 'IOT_'+str(year)+'_ixi/'
    print (year)


    params = json.load(open(__location__+dir+'file_parameters.json'))
    Afile = params['files']['A']
    A = pd.read_csv(__location__+dir+Afile['name'],sep='\t',memory_map=True,skiprows=int(Afile['nr_header']),index_col=list(range(int(Afile['nr_index_col']))))
    Aindex = np.array(list(r for r in A.index))
    A = sp.csr_matrix(A)

    #sudo kill -9 $(pgrep neo4j )


    selector = NodeMatcher(graph)
    countries = selector.match("Country")
    industry = selector.match("Industry")

    ## rm all relationships
    '''
    relation = RelationshipMatcher(graph)
    for i in list(relation.match()):
        graph.delete(i)

    sudo kill -9 $(pgrep neo4j )
    sudo kill -9 $(pgrep python )


    ## remove all industries
    for i in list(list(industry)):
        graph.delete(i)
    '''
    ######################
    # check nodes exist for industries

    industries  = pd.read_csv(__location__+dir+'industries.txt',sep='\t')
    industries.index = [i.split('_')[1] for i in industries['CodeTxt']]

    industry_nodes = set([i[0] for i in graph.run("MATCH (a:Industry) RETURN a.exo_code ").to_ndarray()])

    for missing in set(industries.index) -  industry_nodes:

        print ('creating', missing, 'industry')
        match = industries.loc[missing]

        graph.create(Node("Industry", exo_code=missing, description=match['Name'], exo_CodeNR = match['CodeNr']))



    #################################

    nodes = dict(([i,countries.where("_.alpha3 = '%s'"%i).first()] for i in  set(Aindex[:,0]) ))
    industrynodes  = dict(([i,industry.where("_.description = '%s'"%i).first()] for i in  set(Aindex[:,1]) ))

    nonzero = np.array(A.nonzero()).T

    print 'please wait'

    # do this in parallel

    counter = 0
    try:
        for rel in nonzero:

            weight = A[rel[0],rel[1]]

            source = nodes[Aindex[rel[0]][0]]
            target = nodes[Aindex[rel[1]][0]]

            skip = False
            for test in [source,target]:
                if test == None: skip=True

            if skip:
                print (Aindex[rel[0]][0],Aindex[rel[1]][0],source,target)
                continue

            r = 'Failed on first "Relationship"'
            #inter contry -via intra_industry
            #to_industry

            r = Relationship(
                source,
                'TO_INDUSTRY',
                industrynodes[Aindex[rel[0]][1]],
                year=year,
                target = target['name'],
                weight = weight,
                dataset='exio'
                )
            graph.create(r)

            # intra_industry
            # between industries - industries being the closed system
            r = Relationship(
                industrynodes[Aindex[rel[0]][1]],
                'INTRA_INDUSTRY',
                industrynodes[Aindex[rel[1]][1]],
                year = year,
                source = source['name'],
                target = target['name'],
                weight = weight,
                dataset='exio'
                )
            graph.create(r)


            #inter contry -via intra_industry
            #from_industry
            r = Relationship(
                industrynodes[Aindex[rel[1]][1]],
                'FROM_INDUSTRY',
                target,
                source = source['name'],
                year = year,
                weight = weight,
                dataset='exio'
                )
            graph.create(r)


            counter +=1
    except Exception as e:
        print ('Failed',counter, rel,Aindex[rel[0]],Aindex[rel[1]])
        print ( industrynodes[Aindex[rel[0]][1]],nodes[Aindex[rel[0]][0]])
        print (industrynodes[Aindex[rel[1]][1]],nodes[Aindex[rel[1]][0]])
        print(r,  e )


    print 'adding'



'''
MATCH (a:Country)-[r]-()-[r]->(b:Country)
WITH collect(
    {dsf
        source: id(a),
        target: id(b),
        caption: type(r)
    }
) AS edges
RETURN edges




graph.run(

 MATCH (a:Country)-[r]-(c:Industry {description:'Wool, sil
 k-worm cocoons'})-[r2]-(b:Country)
 WITH collect(
     {
         source: id(a),
         target: id(b),
         caption: type(r),
         weight: r.weight
     }
 ) AS edges
 RETURN edges

 ) .to_ndarray()







'''


print 'done'
