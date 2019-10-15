import pandas as pd
import numpy as np
import json
import scipy.sparse as sp


country  ='IDN'
industry = "Cultivation of oil seeds"



'''add a check if this file has been parsed'''
__location__ = 'data/exiobase/'

#souce country, target country, source industry target insdustry, weight, year
res=[]

for year in range(2005,2012):

    dir = 'IOT_'+str(year)+'_ixi/'
    print (year)


    params = json.load(open(__location__+dir+'file_parameters.json'))
    Afile = params['files']['A']
    A = pd.read_csv(__location__+dir+Afile['name'],sep='\t',memory_map=True,skiprows=int(Afile['nr_header']),index_col=list(range(int(Afile['nr_index_col']))))
    print 'load'
    Aindex = np.array(list(r for r in A.index))
    A = sp.csr_matrix(A)


    for j,i in enumerate(Aindex):
        if list(i) == [country,industry]:
            print 'index', i,j
            index = j



    nonzero = np.array(A.nonzero()).T

    print 'please wait'

    for to in nonzero[nonzero[:,0]== index][:,1]:
        temp = []
        temp.extend(Aindex[index])
        temp.extend(Aindex[to])
        temp.append(A[index,to])
        temp.append(year)

        res.append(temp)




print 'done'
