import networkx as nx
import logging

import sys


class Statistics:
    def __init__(self, graph):
        FORMAT = FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)

        self.graph = graph
        self.nodes_number = 0
        self.edges_number = 0
        self.graph_radius = 0
        self.graph_diameter = 0
        self.graph_density = 0.0
        self.average_in_degree = 0.0
        self.average_out_degree = 0.0
        self.max_in_degree = 0.0
        self.min_in_degree = 0.0
        self.max_out_degree = 0.0
        self.min_out_degree = 0.0
        self.average_weight = 0.0
        self.minimum_weight = 0
        self.maximum_weight = 0
        self.minimum_pageRank = 0.0
        self.maximum_pageRank = 0.0
        self.average_pageRank = 0.0
        self.minimum_betweennessCentrality = 0.0
        self.maximum_betweennessCentrality = 0.0
        self.average_betweennessCentrality = 0.0
        self.sub_graph_diameters = []
        self.sub_graph_radius = []

    def get_statistics(self):

        self.nodes_number = len(self.graph.nodes())
        self.edges_number = len(self.graph.edges())
        self.get_radius()
        self.graph_radius = max(self.sub_graph_radius)
        self.get_diameter()
        self.graph_diameter = max(self.sub_graph_diameters)
        self.graph_density = nx.density(self.graph)
        self.average_in_degree, self.max_in_degree, self.min_in_degree = self.get_average_in_degree()
        self.average_out_degree, self.max_out_degree, self.min_out_degree = self.get_average_out_degree()
        self.average_betweennessCentrality, self.maximum_betweennessCentrality, self.minimum_betweennessCentrality = self.get_average_betweenness_centrality()
        self.average_pageRank, self.maximum_pageRank, self.minimum_pageRank = self.get_average_page_rank()
        self.average_weight, self.maximum_weight, self.minimum_weight = self.get_average_weight()

    def get_diameter(self):
        logging.info("Diameter calculations")
        undirected_graph = nx.DiGraph.to_undirected(self.graph)
        if nx.is_connected(undirected_graph) is False:
            sub_graphs = nx.connected_component_subgraphs(undirected_graph)
            for sg in sub_graphs:
                self.sub_graph_diameters.append(nx.diameter(sg))
        else:
            self.sub_graph_diameters.append(nx.diameter(self.graph))

    def get_radius(self):
        logging.info("Radius calculations")
        undirected_graph = nx.DiGraph.to_undirected(self.graph)
        if nx.is_connected(undirected_graph) is False:
            sub_graphs = nx.connected_component_subgraphs(undirected_graph)
            for sg in sub_graphs:
                self.sub_graph_radius.append(nx.radius(sg))
        else:
            self.sub_graph_radius.append(nx.radius(self.graph))

    def get_average_in_degree(self):
        logging.info("Input degree calculations")
        degree_dictionary = self.graph.in_degree(self.graph.nodes())
        return self.get_average_degree(degree_dictionary)

    def get_average_out_degree(self):
        logging.info("Output degree calculations")
        degree_dictionary = self.graph.out_degree(self.graph.nodes())
        return self.get_average_degree(degree_dictionary)

    def get_average_betweenness_centrality(self):
        logging.info("Betweenness centrality calculations")
        betweenness_centrality_dictionary = nx.betweenness_centrality(self.graph)
        bc_sum = 0.0
        number_of_nodes = len(self.graph.nodes())
        max_betweenness_centrality = 0.0
        min_betweenness_centrality = sys.maxsize

        for value in betweenness_centrality_dictionary.itervalues():
            bc_sum += value
            if max_betweenness_centrality < value:
                max_betweenness_centrality = value
            elif min_betweenness_centrality > value:
                min_betweenness_centrality = value

        return (bc_sum / number_of_nodes), max_betweenness_centrality, min_betweenness_centrality

    def get_average_page_rank(self):
        logging.info("Page rank calculations")
        page_rank_dictionary = nx.pagerank(self.graph)
        pr_sum = 0.0
        number_of_nodes = len(self.graph.nodes())
        max_page_rank = 0.0
        min_page_rank = sys.maxsize

        for value in page_rank_dictionary.itervalues():
            pr_sum += value
            if max_page_rank < value:
                max_page_rank = value
            elif min_page_rank > value:
                min_page_rank = value

        return (pr_sum / number_of_nodes), max_page_rank, min_page_rank

    def get_average_degree(self, degree_dictionary):
        dg_sum = 0
        number_of_nodes = len(self.graph.nodes())
        max_degree = 0
        min_degree = sys.maxsize

        for _, degree in degree_dictionary:
            dg_sum += degree
            if max_degree < degree:
                max_degree = degree
            elif min_degree > degree:
                min_degree = degree

        return (dg_sum / number_of_nodes), max_degree, min_degree

    def get_average_weight(self):
        logging.info("Weight calculations")
        weight_sum = 0
        number_of_nodes = len(self.graph.nodes())
        edges = self.graph.edges(data=True)
        max_weight = 0
        min_weight = sys.maxsize

        for edge in edges:
            attr = edge[2]
            weight = attr['weight']
            weight_sum += weight
            if max_weight < weight:
                max_weight = weight
            elif min_weight > weight:
                min_weight = weight

        return (weight_sum / number_of_nodes), max_weight, min_weight

    def print_statistics(self, filename):

            print "Graph has {} nodes".format(self.nodes_number)
            print "Graph has {} edges".format(self.edges_number)
            print "Max diameter: {}".format(self.graph_diameter)
            print "Max radius: {}".format(self.graph_radius)
            print "Graph density: {}".format(self.graph_density)
            print "Average input degree: {}".format(self.average_in_degree)
            print "Minimal input degree: {}".format(self.min_in_degree)
            print "Maximal input degree: {}".format(self.max_in_degree)
            print "Average output degree: {}".format(self.average_out_degree)
            print "Minimal output degree: {}".format(self.min_out_degree)
            print "Maximal output degree: {}".format(self.max_out_degree)
            print "Average weight: {}".format(self.average_weight)
            print "Minimal weight: {}".format(self.minimum_weight)
            print "Maximal weight: {}".format(self.maximum_weight)
            print "Average page rank: {}".format(self.average_pageRank)
            print "Minimal page rank: {}".format(self.minimum_pageRank)
            print "Maximal page rank: {}".format(self.maximum_pageRank)
            print "Average betweenness centrality: {}".format(self.average_betweennessCentrality)
            print "Minimal betweenness centrality: {}".format(self.minimum_betweennessCentrality)
            print "Maximal betweenness centrality: {}".format(self.maximum_betweennessCentrality)




