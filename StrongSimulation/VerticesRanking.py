import logging
import os
import datetime
import operator
import networkx as nx

from Utils.GraphImportExport import load
from Utils import GraphImportExport as export

DATE_FORMAT = "%Y-%m-%d"


def create_ranking_graphs(graphs_dir, slots_count, number_of_vertices):
    last_end_date = None
    graphs_per_month = []

    i = 1
    j = 1
    while i < slots_count:

        for slot_file in os.listdir(graphs_dir):
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(i) + "_"):
                split = slot_file.split('.')
                split = split[0].split('_')
                if last_end_date is None:
                    last_end_date = split[3]
                month_curr = datetime.datetime.strptime(split[3], DATE_FORMAT).month
                month_last = datetime.datetime.strptime(last_end_date, DATE_FORMAT).month
                logging.info(graphs_dir + slot_file)
                G = load(graphs_dir + slot_file)

                if month_curr != month_last:
                    get_rankings_graph(j, graphs_per_month, last_end_date, number_of_vertices)
                    j += 1
                    graphs_per_month = [G]
                else:
                    graphs_per_month.append(G)

                last_end_date = split[3]
                i += 1


def get_rankings_graph(i, list_of_graphs, date, number_of_vertices):
    ranking_nodes={}

    for graph in list_of_graphs:
        page_rank_dictionary = nx.pagerank(graph)
        sorted_dictionary = dict(sorted(page_rank_dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)[:number_of_vertices])
        for key, value in sorted_dictionary.iteritems():
            if ranking_nodes.has_key(key):
                ranking_nodes[key] += sorted_dictionary[key]
            else:
                ranking_nodes[key] = sorted_dictionary[key]

    sorted_ranking = dict(sorted(ranking_nodes.iteritems(), key=operator.itemgetter(1), reverse=True)[:number_of_vertices])

    G = nx.DiGraph()
    for graph in list_of_graphs:
        subgraph = graph.subgraph(sorted_ranking.keys())
        logging.info("Number of nodes {0}".format(str(len(subgraph.nodes()))))
        G = nx.compose(G, subgraph)

    logging.info("Number of nodes in G {0}".format(str(len(G.nodes()))))
    file_path = '..//Salon24_strongSimulation_final//salon24_{0}_{1}-{2}.json'.format(i, datetime.datetime.strptime(date, DATE_FORMAT).year, datetime.datetime.strptime(date,DATE_FORMAT).month)
    export.save(G, file_path)




