import networkx as nx
import logging
import numpy as np

import sys


class Statistics:
    def __init__(self, graph):
        FORMAT = FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)

        # temporary data
        self.percentiles = [25.0, 50.0, 75.0, 90.0, 95.0, 99.0]
        self.sub_graph_diameters = []
        self.sub_graph_radius = []

        # basic statistics
        self.graph = graph
        self.nodes_number = 0
        self.edges_number = 0
        self.graph_radius = 0
        self.graph_diameter = 0
        self.graph_density = 0.0

        # input degree
        self.average_in_degree = 0.0
        self.max_in_degree = 0.0
        self.min_in_degree = 0.0
        self.in_degree_percentile = []
        self.in_degree_median = 0.0
        self.in_degree_std = 0.0

        # output degree
        self.average_out_degree = 0.0
        self.max_out_degree = 0.0
        self.min_out_degree = 0.0
        self.out_degree_percentile = []
        self.out_degree_median = 0.0
        self.out_degree_std = 0.0

        # output weight
        self.average_weight = 0.0
        self.minimum_weight = 0
        self.maximum_weight = 0
        self.weight_percentile = []
        self.weight_median = 0.0
        self.weight_std = 0.0

        # page rank
        self.minimum_pageRank = 0.0
        self.maximum_pageRank = 0.0
        self.average_pageRank = 0.0
        self.pageRank_percentile = []
        self.pageRank_median = 0.0
        self.pageRank_std = 0.0

        # beetweeness centrality
        self.minimum_betweennessCentrality = 0.0
        self.maximum_betweennessCentrality = 0.0
        self.average_betweennessCentrality = 0.0
        self.betweennessCentrality_percentile = []
        self.betweennessCentrality_median = 0.0
        self.betweennessCentrality_std = 0.0

    def get_statistics(self, get_basic_stats=True, get_radius=True, get_diameter=True, get_in_degree=True,
                       get_out_degree=True, get_betweenness_centrality=True, get_page_rank=True, get_weight=True):

        if get_basic_stats is True:
            self.get_basic_stats()
        if get_radius is True:
            self.get_radius()
        if get_diameter is True:
            self.get_diameter()
        if get_in_degree is True:
            self.get_average_in_degree()
        if get_out_degree is True:
            self.get_average_out_degree()
        if get_betweenness_centrality is True:
            self.get_average_betweenness_centrality()
        if get_page_rank is True:
            self.get_average_page_rank()
        if get_weight is True:
            self.get_average_weight()

    def get_basic_stats(self):
        self.nodes_number = len(self.graph.nodes())
        self.edges_number = len(self.graph.edges())
        self.graph_density = nx.density(self.graph)
        print "Graph has {} nodes".format(self.nodes_number)
        print "Graph has {} edges".format(self.edges_number)
        print "Graph density: {}".format(self.graph_density)

    def get_diameter(self):
        logging.info("Diameter calculations")
        undirected_graph = nx.DiGraph.to_undirected(self.graph)
        if nx.is_connected(undirected_graph) is False:
            sub_graphs = nx.connected_component_subgraphs(undirected_graph)
            for sg in sub_graphs:
                self.sub_graph_diameters.append(nx.diameter(sg))
        else:
            self.sub_graph_diameters.append(nx.diameter(self.graph))

        self.graph_diameter = max(self.sub_graph_diameters)
        print "Max diameter: {}".format(self.graph_diameter)

    def get_radius(self):
        logging.info("Radius calculations")
        undirected_graph = nx.DiGraph.to_undirected(self.graph)
        if nx.is_connected(undirected_graph) is False:
            sub_graphs = nx.connected_component_subgraphs(undirected_graph)
            for sg in sub_graphs:
                self.sub_graph_radius.append(nx.radius(sg))
        else:
            self.sub_graph_radius.append(nx.radius(self.graph))

        self.graph_radius = max(self.sub_graph_radius)
        print "Max radius: {}".format(self.graph_radius)

    def get_average_in_degree(self):
        logging.info("Input degree calculations")
        degree_dictionary = self.graph.in_degree(self.graph.nodes())
        self.average_in_degree, self.max_in_degree, self.min_in_degree, \
        self.in_degree_percentile, self.in_degree_median, self.in_degree_std = self.get_average_degree(
            degree_dictionary)

        print "Average input degree: {}".format(self.average_in_degree)
        print "Minimal input degree: {}".format(self.min_in_degree)
        print "Maximal input degree: {}".format(self.max_in_degree)
        for i in range(0, len(self.percentiles)):
            print "{}-percentile for input degree: {}".format(self.percentiles[i], self.in_degree_percentile[i])
        print "Input degree median: {}".format(self.in_degree_median)
        print "Input degree standard deviation: {}".format(self.in_degree_std)

    def get_average_out_degree(self):
        logging.info("Output degree calculations")
        degree_dictionary = self.graph.out_degree(self.graph.nodes())
        self.average_out_degree, self.max_out_degree, self.min_out_degree, \
        self.out_degree_percentile, self.out_degree_median, self.out_degree_std = self.get_average_degree(
            degree_dictionary)

        print "Average output degree: {}".format(self.average_out_degree)
        print "Minimal output degree: {}".format(self.min_out_degree)
        print "Maximal output degree: {}".format(self.max_out_degree)
        for i in range(0, len(self.percentiles)):
            print "{}-percentile for output degree: {}".format(self.percentiles[i], self.out_degree_percentile[i])
        print "Output degree median: {}".format(self.out_degree_median)
        print "Output degree standard deviation: {}".format(self.out_degree_std)

    def get_average_betweenness_centrality(self):
        logging.info("Betweenness centrality calculations")
        betweenness_centrality_dictionary = nx.betweenness_centrality(self.graph)
        values = []
        for value in betweenness_centrality_dictionary.itervalues():
            values.append(value)

        self.average_betweennessCentrality = np.mean(values)
        self.maximum_betweennessCentrality = max(values)
        self.minimum_betweennessCentrality = min(values)
        self.betweennessCentrality_percentile = np.percentile(values, self.percentiles)
        self.betweennessCentrality_median = np.median(values)
        self.betweennessCentrality_std = np.std(values)

        print "Average betweenness centrality: {}".format(self.average_betweennessCentrality)
        print "Minimal betweenness centrality: {}".format(self.minimum_betweennessCentrality)
        print "Maximal betweenness centrality: {}".format(self.maximum_betweennessCentrality)
        for i in range(0, len(self.percentiles)):
            print "{}-percentile for betweenness centrality: {}".format(self.percentiles[i],
                                                                        self.betweennessCentrality_percentile[i])
        print "Betweenness centrality median: {}".format(self.betweennessCentrality_median)
        print "Betweenness centrality standard deviation: {}".format(self.betweennessCentrality_std)

    def get_average_page_rank(self):
        logging.info("Page rank calculations")
        page_rank_dictionary = nx.pagerank(self.graph)
        values = []
        for value in page_rank_dictionary.itervalues():
            values.append(value)

        self.average_pageRank = np.mean(values)
        self.minimum_pageRank = min(values)
        self.maximum_pageRank = max(values)
        self.pageRank_percentile = np.percentile(values, self.percentiles)
        self.pageRank_median = np.median(values)
        self.pageRank_std = np.std(values)

        print "Average Page Rank: {}".format(self.average_pageRank)
        print "Minimal Page Rank: {}".format(self.minimum_pageRank)
        print "Maximal Page Rank: {}".format(self.maximum_pageRank)
        for i in range(0, len(self.percentiles)):
            print "{}-percentile for Page Rank: {}".format(self.percentiles[i],
                                                           self.pageRank_percentile[i])
        print "Page Rank median {}".format(self.pageRank_median)
        print "Page Rank standard deviation {}".format(self.pageRank_std)

    def get_average_degree(self, degree_dictionary):
        degrees_list = []
        for _, degree in degree_dictionary:
            degrees_list.append(degree)

        return np.mean(degrees_list), max(degrees_list), min(degrees_list), np.percentile(degrees_list,
                                                                                          self.percentiles), np.median(
            degrees_list), np.std(degrees_list)

    def get_average_weight(self):
        logging.info("Weight calculations")
        edges = self.graph.edges(data=True)
        weight_values = []

        for edge in edges:
            attr = edge[2]
            weight = attr['weight']
            weight_values.append(weight)

        self.minimum_weight = min(weight_values)
        self.maximum_weight = max(weight_values)
        self.average_weight = np.mean(weight_values)
        self.weight_percentile = np.percentile(weight_values, self.percentiles)
        self.weight_median = np.median(weight_values)
        self.weight_std = np.std(weight_values)

        print "Average weight: {}".format(self.average_weight)
        print "Minimal weight: {}".format(self.minimum_weight)
        print "Maximal weight: {}".format(self.maximum_weight)
        for i in range(0, len(self.percentiles)):
            print "{}-percentile for weight: {}".format(self.percentiles[i],
                                                        self.weight_percentile[i])
        print "Weight median: {}".format(self.weight_median)
        print "Weight standard deviation: {}".format(self.weight_std)

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
