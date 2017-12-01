import networkx as nx
import logging

import Model.DatabaseConnection as dbConn
from Utils import GraphImportExport as importExport
from Utils import GraphStatistics as statistics


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
conn = dbConn.connect()
logging.info("Connected to salon24 database")
G = nx.Graph();
G = dbConn.create_social_network(conn)
logging.info("Social network graph created")
statistics = statistics.Statistics(G)
statistics.get_statistics()



# importExport.save(G, "test.json")
# imported_graph = importExport.load("test.json")

