import logging
import os
import csv
import sys
import GraphStatistics as statistics

from GraphImportExport import load


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
           str(avg_out_degree_difference) + "," + str(avg_page_rank_difference) + "," + str(avg_weight_difference) + "\n"

    out_file.write(line)
