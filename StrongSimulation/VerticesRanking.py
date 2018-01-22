import logging
import os
import datetime
import operator
import networkx as nx

from Utils.GraphImportExport import load
from Utils import GraphImportExport as export

DATE_FORMAT = "%Y-%m-%d"


def create_ranking_graphs(graphs_dir, results_dir, slots_count, number_of_vertices):
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
                    get_rankings_graph(results_dir, j, graphs_per_month, last_end_date, number_of_vertices)
                    j += 1
                    graphs_per_month = [G]
                else:
                    graphs_per_month.append(G)

                last_end_date = split[3]
                i += 1


def create_ranking_graphs_weeks(graphs_dir, result_dir, slots_count, number_of_vertices):

    i = 1
    while i < slots_count:
        for slot_file in os.listdir(graphs_dir):
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(i) + "_"):
                split = slot_file.split('.')
                split = split[0].split('_')
                idx = split[1]
                date_from = split[2]
                date_to = split[3]
                logging.info(graphs_dir + slot_file)
                G = load(graphs_dir + slot_file)

                get_ranking_graphs_weeks(result_dir, idx, G, date_from, date_to, number_of_vertices)
                i += 1


def get_rankings_graph(results_dir, i, list_of_graphs, date, number_of_vertices):
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

    G1 = G.to_undirected()
    connected_components = sorted(nx.connected_components(G1), key=len, reverse=True)
    logging.info("Number of connected components : {0}".format(str(len(connected_components))))

    H = G.subgraph(connected_components[0])
    logging.info("Number of nodes in G {0}".format(str(len(H.nodes()))))
    file_path = results_dir + '\\salon24_{0}_{1}-{2}.json'.format(i, datetime.datetime.strptime(date, DATE_FORMAT).year, datetime.datetime.strptime(date,DATE_FORMAT).month)
    export.save(H, file_path)


def get_ranking_graphs_weeks(results_dir, i, graph, date_from, date_to, number_of_vertices):

    page_rank_dictionary = nx.pagerank(graph)
    sorted_dictionary = dict(sorted(page_rank_dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)[:number_of_vertices])

    G = graph.subgraph(sorted_dictionary.keys())
    logging.info("Number of nodes {0}".format(str(len(G.nodes()))))

    G1 = G.to_undirected()
    connected_components = sorted(nx.connected_components(G1), key=len, reverse=True)
    logging.info("Number of connected components : {0}".format(str(len(connected_components))))

    H = G.subgraph(connected_components[0])
    logging.info("Number of nodes in G {0}".format(str(len(H.nodes()))))
    start = datetime.datetime.strptime(date_from, DATE_FORMAT)
    end = datetime.datetime.strptime(date_to, DATE_FORMAT)
    file_path = results_dir + '//salon24_{0}_{1}_{2}.json'.format(i, start.date(), end.date())
    export.save(H, file_path)

