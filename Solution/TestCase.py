import os
import logging
from Solution import OwnAlgorithm
from Utils.GraphImportExport import load

DATE_FORMAT = "%Y-%m-%d"


class MatchStructure:

    def __init__(self, G, idx, date, date_from, date_to):
        self.G = G
        self.idx = idx
        self.date = date
        self.date_from = date_from
        self.date_to = date_to


def perform_test(graphs_dir, number_from, result_file, slots_count):
    previous = None

    while number_from <= slots_count:
        for slot_file in os.listdir(graphs_dir):
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(number_from) + "_"):
                logging.info(graphs_dir + slot_file)
                split = slot_file.split('.')
                split = split[0].split('_')
                idx = split[1]
                month = split[2]
                G = load(graphs_dir + slot_file)
                current = MatchStructure(G, idx, month)
                if previous is not None:
                    match_slots(previous, current, result_file)
                number_from += 1
                previous = current


def perform_test2(graphs_dir1, graphs_dir2, number_from, result_file, slots_count):
    while number_from < slots_count:
        for slot_file in os.listdir(graphs_dir1):
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(number_from) + "_"):
                logging.info(graphs_dir1 + slot_file)
                split = slot_file.split('.')
                split = split[0].split('_')
                idx = split[1]
                date_from = split[2]
                date_to = split[3]
                G = load(graphs_dir1 + slot_file)
                previous = MatchStructure(G, idx, None, date_from, date_to)
                number_from += 1
                for slot_file1 in os.listdir(graphs_dir2):
                    if slot_file1.endswith(".json") and slot_file1.startswith("salon24_" + str(number_from) + "_"):
                        logging.info(graphs_dir2 + slot_file1)
                        split1 = slot_file1.split('.')
                        split1 = split1[0].split('_')
                        idx1 = split1[1]
                        date_from1 = split1[2]
                        date_to1 = split1[3]
                        G1 = load(graphs_dir2 + slot_file1)
                        current = MatchStructure(G1, idx1, None, date_from1, date_to1)
                        match_slots(previous, current, result_file, idx1)


def match_slots(previous, current, result_file, id):
    out_file = open(result_file, 'a')
    algorithm = OwnAlgorithm.Algorithm(previous.G, current.G, 0.25, 0.50, 5, id)
    result = algorithm.run_algorithm()

    if len(result.nodes()) > 0:
        line = str(previous.idx) + "," + str(previous.date_from) + " - " + str(previous.date_to) + "," + str(
            current.idx) + "," + str(current.date_from) + " - " + str(current.date_to) + "," + \
               "1" + "," + str(compare_graphs(previous.G, result)) + "\n"
        out_file.write(line)
    else:
        line = str(previous.idx) + "," + str(previous.date_from) + " - " + str(previous.date_to) + "," + str(
            current.idx) + "," + str(current.date_from) + " - " + str(current.date_to) + "," + \
               "0" + "," + str(compare_graphs(previous.G, current.G)) + "\n"
        out_file.write(line)

    out_file.close()


def compare_graphs(G1, G2):
    not_matched = 0
    not_matched_vertices = 0
    for edge in G1.edges():
        if not G2.has_edge(edge[0], edge[1]):
            not_matched += 1

    for vertex in G1.nodes():
        if not G2.has_node(vertex):
            not_matched_vertices += 1

    matched = len(G1.edges()) - not_matched
    percent_of_edges = float(matched) / float(len(G1.edges())) * 100.0
    matched_vertices = len(G1.nodes()) - not_matched_vertices
    percent_of_nodes = float(matched_vertices) / float(len(G1.nodes())) * 100.0

    return str(not_matched) + "," + str(not_matched_vertices) + "," + str(percent_of_edges) + "," + str(
        percent_of_nodes)


def write_stats(file_name, previous, current, vertices_intersection, percent_of_edges, number_of_missing_edges, weeks):
    result_file = open(file_name, 'a')

    percent_of_covered_vertices = float(len(vertices_intersection)) / float(len(previous.G.nodes())) * 100.0

    if weeks is False:
        line = str(previous.idx) + "," + str(previous.date) + "," + str(current.idx) + "," + str(current.date) + \
               "," + str(len(previous.G.nodes())) + "," + str(len(current.G.nodes())) + "," + \
               str(len(vertices_intersection)) + "," + str(percent_of_covered_vertices) + "," + str(percent_of_edges) + \
               "," + str(number_of_missing_edges) + "\n"
    else:
        line = str(previous.idx) + "," + str(previous.date_from) + "," + str(previous.date_to) + "," + str(current.idx) \
               + "," + str(current.date_from) + "," + str(current.date_to) + "," + str(len(previous.G.nodes())) + "," \
               + str(len(current.G.nodes())) + "," + str(len(vertices_intersection)) + \
               "," + str(percent_of_covered_vertices) + "," + \
               str(percent_of_edges) + "," + str(number_of_missing_edges) + "\n"

    result_file.write(line)
    result_file.close()
