import networkx as nx
import logging
import os

import Salon24Model.DatabaseConnection as dbConn
from Utils import GraphImportExport as importExport
from Utils import GraphStatistics as statistics
from AmazonModel import AmazonGraphBuilder as amazonModel
from Utils import TimeSlotsStatistics as timeSlotStats
from StrongSimulation import StrongSimulation as strongSimulation



# FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
# logging.basicConfig(format=FORMAT, level=logging.INFO)
# conn = dbConn.connect()
# logging.info("Connected to salon24 database")
# G = dbConn.create_social_network(conn)
# logging.info("Social network graph created")
# statistics = statistics.Statistics(G)
# #statistics.get_statistics(get_diameter=False, get_radius=False, get_basic_stats=False)
# statistics.get_statistics()


# script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
# path = amazonModel.get_file_path(script_dir)
# AmazonGraph = amazonModel.build_graph(path)
# # importExport.save(AmazonGraph, "Resources//Amazon.json")
# amazonStatistics = statistics.Statistics(AmazonGraph)
# amazonStatistics.get_statistics(get_basic_stats=False, get_weight=False, get_diameter=False, get_radius=True, get_page_rank=False,
#                                 get_in_degree=False, get_out_degree=False, get_betweenness_centrality=False)

# timeSlotStats.get_stats_for_dynamic_graphs("..\\Salon24_TimeSlots\\", 671)
# timeSlotStats.get_percentage_changes_for_slots("salon24_slots.csv")
#timeSlotStats.get_graph_structure_stats("..\\Salon24_TimeSlots\\", 671)
# dbConn.create_dynamic_graphs_for_salon24()


# importExport.save(G, "test.json")
# imported_graph = importExport.load("test.json")

number_of_edges = 251
number_of_nodes = 100
number_of_query_nodes = 6
number_of_query_edges = 9

G = nx.fast_gnp_random_graph(number_of_nodes, number_of_edges, directed=True)
Q = nx.fast_gnp_random_graph(number_of_query_nodes, number_of_query_edges, directed= True)
query_diameter = nx.diameter(Q)

strongSimulation = strongSimulation.StrongSimulation(Q, G, query_diameter)
matches = strongSimulation.match()
print 'kupka'