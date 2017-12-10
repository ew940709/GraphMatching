import networkx as nx
import logging
import os

import Salon24Model.DatabaseConnection as dbConn
from Utils import GraphImportExport as importExport
from Utils import GraphStatistics as statistics
from AmazonModel import AmazonGraphBuilder as amazonModel
from Utils import TimeSlotsStatistics as timeSlotStats



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

timeSlotStats.get_stats_for_dynamic_graphs("..\\Salon24_TimeSlots\\", 671)

# dbConn.create_dynamic_graphs_for_salon24()


# importExport.save(G, "test.json")
# imported_graph = importExport.load("test.json")

