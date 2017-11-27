import networkx as nx

import Model.DatabaseConnection as dbConn
from Utils import GraphImportExport as importExport

conn = dbConn.connect()

G = nx.Graph();


G = dbConn.create_social_network(conn)


print "Number of edges " + str(len(G.edges()))
print "Number of nodes " + str(len(G.nodes()))


importExport.save(G, "test.json")
imported_graph = importExport.load("test.json")

