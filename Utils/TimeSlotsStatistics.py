import logging
import os
import csv
import GraphStatistics as statistics

from GraphImportExport import load


class TimeSlot:
    def __init__(self, graph, graph_id, date_from, date_to):
        self.graph = graph
        self.graph_id = graph_id
        self.date_from = date_from
        self.date_to = date_to


def get_stats_for_dynamic_graphs(graphs_dir, count):
    out_file = open("salon24_slots.csv", 'a')
    write_headers_to_file(out_file)

    i = 1
    while i < count:
        for slot_file in os.listdir(graphs_dir):
            logging.info(graphs_dir + slot_file)
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(i) + "_"):
                split = slot_file.split('.')
                split = split[0].split('_')
                idx = split[1]
                date_from = split[2]
                date_to = split[3]
                logging.info(graphs_dir + slot_file)
                G = load(graphs_dir + slot_file)
                stats = statistics.Statistics(G)
                stats.get_statistics(get_betweenness_centrality=False, get_radius=False, get_diameter=False)
                write_statistics_to_csv(out_file, stats, idx, date_from, date_to)
                i += 1

    out_file.close()


def get_graph_structure_stats(graphs_dir, count):
    out_file = open("salon24_slots_structure.csv", 'a')
    write_headers_structure_to_file(out_file)

    i = 1
    while i < count:
        for slot_file in os.listdir(graphs_dir):
            logging.info(graphs_dir + slot_file)
            if slot_file.endswith(".json") and slot_file.startswith("salon24_" + str(i) + "_"):
                split = slot_file.split('.')
                split = split[0].split('_')
                idx = split[1]
                date_from = split[2]
                date_to = split[3]
                logging.info(graphs_dir + slot_file)
                graph = load(graphs_dir + slot_file)
                slot = TimeSlot(graph, idx, date_from, date_to)
                if i > 1:
                    write_structure_difference_to_csv(out_file, last_slot, slot)
                last_slot = slot
                i += 1

    out_file.close()


def get_percentage_changes_for_slots(csv_file):
    f = open(csv_file, 'rb')
    out_file = open("salon24_slots_percentage_diff.csv", 'a')
    write_headers_to_csv(out_file)
    reader = csv.reader(f)

    row_num = 0
    last_row = ""
    for row in reader:
        if row_num == 1:
            last_row = row
        elif row_num > 1:
            percent_difference_to_csv(out_file, last_row, row)
            last_row = row
        row_num += 1
    f.close()
    out_file.close()


def write_headers_to_file(csv_file):
    header = "id,date_from,date_to,"
    basics_stats = "number of nodes,number of edges,density,"
    in_degree = "average_in_degree,min_in_degree,max_in_degree,25.0 percentile input degree," \
                "50.0 percentile input degree,75.0 percentile input degree,90.0 percentile input degree," \
                "95.0 percentile input degree,99.0 percentile input degree,input degree median," \
                "input degree standard deviation,"
    out_degree = "average_out_degree,min_out_degree,max_out_degree,25.0 percentile output degree," \
                 "50.0 percentile out degree,75.0 percentile out degree,90.0 percentile out degree," \
                 "95.0 percentile out degree,99.0 percentile out degree," \
                 "output degree median,output degree standard deviation,"
    page_rank = "average_page_rank,min_page_rank,max_page_rank,25.0 percentile page rank," \
                "50.0 percentile page rank,75.0 percentile page rank,90.0 percentile page rank," \
                "95.0 percentile page rank,99.0 percentile page rank," \
                "page rank median,page rank standard deviation,"
    weight = "average_weight,min_weight,max_weight,25.0 percentile weight," \
             "50.0 percentile weight,75.0 percentile weight,90.0 percentile weight," \
             "95.0 percentile weight,99.0 percentile weight," \
             "weight median,weight standard deviation\n"

    full_header = header + basics_stats + in_degree + out_degree + page_rank + weight
    csv_file.write(full_header)


def write_statistics_to_csv(csv_file, stats, id, date_from, date_to):
    header = str(id) + "," + str(date_from) + "," + str(date_to) + ","
    basic_stats = str(stats.nodes_number) + "," + str(stats.edges_number) + "," + str(stats.graph_density) + ","
    in_degree = stats.in_degree_str()
    out_degree = stats.out_degree_str()
    page_rank = stats.page_rank_str()
    weight = stats.weight_str()

    line = header + basic_stats + str(in_degree) + "," + str(out_degree) + "," + str(page_rank) + "," + str(
        weight) + "\n"
    csv_file.write(line)


def write_headers_to_csv(csv_file):
    header = "graph_id,last row date range,current row date range,"
    stats = "nodes_difference,edges difference,density difference,input degree difference," \
            "output degree difference,page rank difference,weight difference"

    line = header + stats + "\n"
    csv_file.write(line)


def percent_difference_to_csv(out_file, last_row, row):
    row_id = str(last_row[0]) + "->" + str(row[0])
    last_row_date = str(last_row[1]) + " - " + last_row[2]
    row_date = str(row[1]) + " - " + row[2]
    nodes_difference = ((float(row[3]) - float(last_row[3])) / float(last_row[3])) * 100.0
    edges_difference = ((float(row[4]) - float(last_row[4])) / float(last_row[4])) * 100.0
    density_difference = ((float(row[5]) - float(last_row[5])) / float(last_row[5])) * 100.0
    avg_in_degree_difference = ((float(row[6]) - float(last_row[6])) / float(last_row[6])) * 100.0
    avg_out_degree_difference = ((float(row[17]) - float(last_row[17])) / float(last_row[17])) * 100.0
    avg_page_rank_difference = ((float(row[28]) - float(last_row[28])) / float(last_row[28])) * 100.0
    avg_weight_difference = ((float(row[39]) - float(last_row[39])) / float(last_row[39])) * 100.0

    line = row_id + "," + last_row_date + "," + row_date + "," + str(nodes_difference) + "," + \
           str(edges_difference) + "," + str(density_difference) + "," + str(avg_in_degree_difference) + "," + \
           str(avg_out_degree_difference) + "," + str(avg_page_rank_difference) + "," + str(
        avg_weight_difference) + "\n"

    out_file.write(line)


def write_headers_structure_to_file(out_file):
    header = "id,last slot date range,current slot date range," \
             "number of nodes in last slot,number of nodes in current slot,active nodes," \
             "number of edges in last slot,number of edges in current slot,active edges\n"

    out_file.write(header)


def write_structure_difference_to_csv(out_file, last_slot, slot):
    active_nodes = get_active_nodes(last_slot.graph, slot.graph)
    active_edges = get_active_edges(last_slot.graph, slot.graph)
    line_id = str(last_slot.graph_id) + "->" + str(slot.graph_id)
    last_date_range = str(last_slot.date_from) + " - " + str(last_slot.date_to)
    current_date_range = str(slot.date_from) + " - " + str(slot.date_to)
    last_slot_nodes_count = len(last_slot.graph.nodes())
    current_slot_nodes_count = len(slot.graph.nodes())
    last_slot_edges_count = len(last_slot.graph.edges())
    current_slot_edges_count = len(slot.graph.edges())

    line = line_id + "," + last_date_range + "," + current_date_range + "," + str(last_slot_nodes_count) + "," \
           + str(current_slot_nodes_count) + "," + str(active_nodes) + "," + str(last_slot_edges_count) + "," + \
           str(current_slot_edges_count) + "," + str(active_edges) + "\n"

    out_file.write(line)


def get_active_nodes(last_graph, graph):
    active_nodes_counter = 0
    for node in last_graph.nodes():
        if graph.has_node(node) is True:
            active_nodes_counter += 1

    return active_nodes_counter


def get_active_edges(last_graph, graph):
    active_edges_counter = 0
    for edge in last_graph.edges():
        if graph.has_edge(edge[0], edge[1]) is True:
            active_edges_counter += 1

    return active_edges_counter
