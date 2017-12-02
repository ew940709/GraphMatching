import networkx as nx
import os

FILE_NAME = "Amazon0302.txt"
FILE_REL_PATH = 'Resources\\Amazon0302.txt'


def get_file_path(script_dir):
    path = os.path.relpath(FILE_REL_PATH, script_dir)
    return path


def build_graph(path):
    graph = nx.DiGraph()
    try:
        graph_data_file = open(path, "r")

        for line in graph_data_file:
            if line[0] != '#':
                nodes = line.split()
                graph.add_edge(nodes[0], nodes[1])

        graph_data_file.close()

    except (Exception, IOError) as error:
        print(error)

    return graph
