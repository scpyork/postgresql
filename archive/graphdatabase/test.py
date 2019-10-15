'sudo neo4j start'
'default neo4j:neo4j'

#https://medium.com/neo4j/py2neo-v4-2bedc8afef2


from py2neo import Graph,Node,Relationship,NodeMatcher

graph =  Graph("http://localhost:7474/db/data/",
 user="neo4j", password="sei")

#(graph name is data)
#from chrome  http://localhost:7474/browser/

#graph.run('MATCH (a:Person) RETURN a.name, a.born LIMIT")

#Relationship(start_node, type, end_node, **properties)


alice =  Node("Person", name="Alice",likes ='log')
graph.create(alice)


b =  Node("Person", name="bob",blob ='hi')
graph.create(b)




def mergenodes(nodes, graph):
    '''merges nodes and removes old
       properties of first node override those of all others:

       nodes is a list of matches e.g.
       list(NodeMatcher(graph).match('Person').where("_.name='Alice'"))

    '''
    propertydict = {}

    for n in nodes[::-1]:
        for k in n.keys():
            v = n[k]
            if v != None:
                propertydict[k] = v

    mainnode = nodes[0]
    print  propertydict
    for k in propertydict:
        print k, mainnode,mainnode[k]
        mainnode[k]=propertydict[k]

    graph.merge(mainnode)
    graph.push(mainnode)

    for n in nodes[1:]:
        graph.delete(n)


mergenodes(list(NodeMatcher(graph).match('Person').where("_.name='Alice'")),graph)
















#updating a property
c = NodeMatcher(graph).match('Person',blob='hi').first()

c['name']= 'plonk'
graph.merge(c)
graph.push(c)


selector = NodeMatcher(graph)
selected = selector.match("Person")
me = selected.where("_.name > 'a'",)

print list(me)

##or

graph.run("MATCH (a:Person) WHERE a.name > 'a' RETURN a.name LIMIT 3").to_table()


##or

list(selector.match("Person").where("_.name =~ 'K.*'")
    .order_by("_.name").limit(3))


npeople = graph.evaluate("MATCH (a:Person) RETURN count(a)")

[(a["name"], a["born"])
     for a in graph.nodes.match("Person").limit(3)]

list(graph.nodes.match())

##https://medium.com/neo4j/py2neo-v4-2bedc8afef2

# to clear graph.delete_all?

#_ refers to node being filtered
#selector = NodeSelector(graph)
# selected = selector.select("Person").where("_.name =~ 'J.*'", "1960 <= _.born < 1970")
#selection.where(born=1976)
#>>> list(selected)
#match many cypher



#cypher to subgraph


'''
MATCH (a)-[r]->(b)
WITH collect(
    {
        source: id(a),
        target: id(b),
        caption: type(r)
    }
) AS edges
RETURN edges
'''


'''
>>> keanu = graph.nodes.match("Person", name="Keanu Reeves").first()
>>> list(graph.relationships.match((keanu, None), "ACTED_IN")
              .limit(3))
'''
'''
reuse relationship type
mary_poppins = Node("Movie", title="Mary Poppins")
>>> ACTED_IN = Relationship.type("ACTED_IN")
>>> graph.create(ACTED_IN(keanu, mary_poppins))
>>> graph.match((keanu, mary_poppins)).first()
(Keanu Reeves)-[:ACTED_IN {}]->(_189)
'''
