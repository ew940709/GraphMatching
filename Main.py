import Queue

import networkx as nx
import matplotlib.pyplot as plt
import logging
import os

import numpy

import Salon24Model.DatabaseConnection as dbConn
import StrongSimulation.VerticesRanking as ranking
import StrongSimulation.TestCase as test
import TALE.TestCase as taleTest
import Solution.TestCase as testCase

from StrongSimulation.VerticesRanking import Measure
from Utils import GraphImportExport as importExport
from Utils import GraphStatistics as statistics
from AmazonModel import AmazonGraphBuilder as amazonModel
from Utils import TimeSlotsStatistics as timeSlotStats
from StrongSimulation import StrongSimulation as strongSimulation
from Salon24Model import TagsRanking as tagsRanking
from TALE import TaleAlgorithm as tale

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
# timeSlotStats.get_graph_structure_stats("..\\Salon24_TimeSlots\\", 671)
# dbConn.create_dynamic_graphs_for_salon24()


# importExport.save(G, "test.json")
# imported_graph = importExport.load("test.json")

# number_of_edges = 251
# number_of_nodes = 100
# number_of_query_nodes = 6
# number_of_query_edges = 9
#
# G = nx.fast_gnp_random_graph(number_of_nodes, number_of_edges, directed=True)
# Q = nx.fast_gnp_random_graph(number_of_query_nodes, number_of_query_edges, directed= True)
# query_diameter = nx.diameter(Q)
#
# strongSimulation = strongSimulation.StrongSimulation(Q, G, query_diameter)
# matches = strongSimulation.match()

# G1 = nx.DiGraph()
# G1.add_edge('HR', 'SE')
# G1.add_edge('HR', 'Bio')
# G1.add_edge('SE', 'Bio')
# G1.add_edge('DM', 'Bio')
# G1.add_edge('AI', 'DM')
# G1.add_edge('DM', 'AI')
#
# Q1 = nx.DiGraph()
# Q1.add_edge('AI', 'DM')
# Q1.add_edge('DM', 'AI')
# Q1.add_edge('DM', 'Bio')
# Q1.add_edge('HR', 'Bio')
# Q1.add_edge('HR', 'SE')
# Q1.add_edge('SE', 'Bio')
#
#
# query2 = Q1.to_undirected()
# query_diameter = nx.diameter(query2)
#
# strongSimulation1 = strongSimulation.StrongSimulation(Q1, G1, query_diameter)
# matches = strongSimulation1.match()


# dbConn.create_dynamic_graphs_strong_simulation_salon24()
# ranking.create_ranking_graphs("..\\Salon24_TimeSlots_strongSimulation\\", "..\\Salon24_strongSimulation_final_20", 252, 20)
# ranking.create_ranking_graphs("..\\Salon24_TimeSlots_strongSimulation\\", "..\\Salon24_strongSimulation_final_10", 252, 10)
# test.perform_test2("..\\Salon24_strongSimulation_final_10\\", "..\\Salon24_strongSimulation_final_20\\", 1, "Resources\\StrongSimulation_results.csv", 10)


#
# G = importExport.load("..\\Salon24_strongSimulation_final\\salon24_1_2008-1.json")
# # nx.draw(G, with_labels=True)
# # plt.show()
# nodes1 = G.nodes()

#
# G1 = importExport.load("..\\Salon24_strongSimulation_final\\salon24_2_2008-2.json")
# # nx.draw(G1, with_labels=True)
# # plt.show()
#
# nodes2 = G1.nodes()
#
# nodes_intersection = set(nodes1).intersection(nodes2)
# print len(nodes_intersection)
#
# G2 = importExport.load("..\\Salon24_strongSimulation_final\\salon24_3_2008-3.json")
# # nx.draw(G2, with_labels=True)
# # plt.show()
#
# nodes3 = G2.nodes()
# nodes_intersection2 = set(nodes2).intersection(nodes3)
# print len(nodes_intersection2)


# test.perform_stats_test("..\\Salon24_strongSimulation_final_10\\", 1, "Resources\\Comparision_10.csv", 66)
# test.perform_stats_test("..\\Salon24_strongSimulation_final_20\\", 1, "Resources\\Comparision_20.csv", 66)


# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_10\\", 671, 10, Measure.PAGE_RANK)
# #test.perform_stats_test_week("..\\Salon24_ranking_weeks_10\\", 1, "Resources\\Comparision_weeks_10.csv", 671)
#
# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_20\\", 671, 20, Measure.PAGE_RANK)
# #test.perform_stats_test_week("..\\Salon24_ranking_weeks_20\\", 1, "Resources\\Comparision_weeks_20.csv", 671)
#
# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_10_weight\\", 671, 10, Measure.VERTICES_IN)
# test.perform_stats_test_week("..\\Salon24_ranking_weeks_10_weight\\", 1, "Resources\\Comparision_weeks_10_weight.csv", 671)
#

# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_20_weight_comp\\", 671, 20, Measure.VERTICES_IN)
# test.perform_stats_test_week("..\\Salon24_ranking_weeks_20_weight\\", 1, "Resources\\Comparision_weeks_20_weight.csv", 671)

# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_10_comp\\", 671, 10, Measure.PAGE_RANK)
# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_20_comp\\", 671, 20, Measure.PAGE_RANK)
# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_100_comp\\", 671, 100, Measure.PAGE_RANK)
# ranking.create_ranking_graphs_weeks("..\\Salon24_TimeSlots\\", "..\\Salon24_ranking_weeks_100_weight_comp\\", 671, 100, Measure.VERTICES_IN)
#
# test.perform_test2("..\\Salon24_ranking_weeks_10_comp\\", "..\\Salon24_ranking_weeks_10_comp\\", 1, "Resources\\StrongSimulation_results_10_comp.csv", 671)
# test.perform_test2("..\\Salon24_ranking_weeks_10_comp\\", "..\\Salon24_ranking_weeks_20_comp\\", 1, "Resources\\StrongSimulation_results_10_comp_20.csv", 671)
# test.perform_test2("..\\Salon24_ranking_weeks_20_comp\\", "..\\Salon24_ranking_weeks_20_comp\\", 1, "Resources\\StrongSimulation_results_20_comp_20.csv", 671)


# tagsRanking.get_most_commented_posts_for_dynamic_graph(669, 20, "..\\Salon24_top_posts_pagerank")
# tagsRanking.get_most_commented_posts_for_dynamic_graph(670, 20, "..\\Salon24_top_posts_pagerank")

# tale = tale.Tale(nx.Graph())
# a = numpy.array([[0,0,1], [0,1,0]], dtype=bool)
# # print(a[1][-1])
#

# taleTest.perform_test2("..\\Salon24_ranking_weeks_10_weight\\", "..\\Salon24_ranking_weeks_20_weight\\", 1,
#                    "Resources\\Tale_results_10_comp_20_weight.csv", 671)


# taleTest.perform_test2("..\\Salon24_TimeSlots\\", "..\\Salon24_TimeSlots\\", 1,
#                    "Resources\\Tale_results.csv", 671)
#
# taleTest.perform_test2("..\\Salon24_ranking_weeks_10\\", "..\\Salon24_ranking_weeks_20\\", 1,
#                     "Resources\\Tale_results_10_comp_20.csv", 671)

# tagsRanking.get_most_popular_tags("..\\Salon24_TimeSlots\\", 1, 671, 20, "Resources")


#testCase.perform_test2("../Salon24_ranking_weeks_10_weight/", "../Salon24_ranking_weeks_20_weight/", 1 , "Resources/Algorithm_v1_results_10_comp_20_weight.csv",
#                       671)

testCase.perform_test2("..\\Salon24_TimeSlots\\", "..\\Salon24_TimeSlots\\", 300 , "Resources\\Algorithm_v2_results.csv",
                         671)

