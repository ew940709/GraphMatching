import DatabaseConnection as db_conn
import GraphImportExport as import_export
import networkx as nx

conn = db_conn.connect()

G = nx.Graph();


G = db_conn.create_social_network(conn)


print "Number of edges " + str(len(G.edges()))
print "Number of nodes " + str(len(G.nodes()))


import_export.save(G, "test.json")
imported_graph = import_export.load("test.json")

