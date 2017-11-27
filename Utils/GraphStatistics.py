import networkx as nx


def get_statistics(graph):
    #create class 
    nodes_number = len(graph.nodes())
    edges_number = len(graph.edges())
    graph_radius = nx.radius(graph)
    graph_diameter = nx.diameter(graph)
    graph_density = nx.density(graph)
    average_in_degree, max_in_degree, min_in_degree = get_average_in_degree(graph)
    average_out_degree, max_in_degree, min_in_degree = get_average_out_degree(graph)


def get_average_in_degree(graph):
    degree_dictionary = nx.in_degree(graph.nodes())
    return count_average(graph, degree_dictionary)


def get_average_out_degree(graph):
    degree_dictionary = nx.out_degree(graph.nodes())
    return count_average(graph, degree_dictionary)


def count_average(graph, degree_dictionary):
    sum = 0
    number_of_nodes = len(graph.nodes())
    max_degree = 0
    min_degree = 0

    for node in degree_dictionary:
        sum += degree_dictionary[node]
        if max_degree < degree_dictionary[node]:
            max_degree = degree_dictionary[node]
        elif min_degree < degree_dictionary[node]:
            min_degree = degree_dictionary[node]

    return (sum / number_of_nodes), max_degree, min_degree
