import Queue
import logging
import math
import numpy
import operator
import networkx as nx
import cPickle as pickle

from Solution.DisjointSet import DisjointSet
from TALE import NHIndex


class Algorithm:

    def __init__(self, query_graph, db_graph, p, importance_threshold, max_hops, index):
        FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        self.query_graph = query_graph
        self.db_graph = db_graph
        self.p = p
        self.max_hops = max_hops
        self.importance_threshold = importance_threshold
        self.index = index
        self.query_dictionary = {}
        self.bitmap = self.create_bitmap()
        self.set, self.dict = self.set_disjoint_set_for_graph()

    def run_algorithm(self):
        logging.info("Algorithm run method started")
        logging.info("Algorithm selecting important nodes")
        important_nodes = self.get_important_nodes(False)
        logging.info("Algorithm bitmap probing")

        worth_nodes = []
        for node in important_nodes:
            if self.query_dictionary.has_key(node[0]):
                actual_node = node[0]
                result = self.bitmap_probe(self.query_dictionary[actual_node], self.bitmap[actual_node][1], 1,
                                           len(self.bitmap[actual_node][0]),
                                           self.p)
                if result[0] == 1:
                    worth_nodes.append(node[0])

        M_imp = self.db_graph.subgraph(worth_nodes)

        logging.info("Algorithm matching")
        match = self.grow_match(M_imp, self.query_dictionary, self.bitmap)
        return match

    def create_bitmap(self):
        result = {}

        # creating list of all nodes
        list_nodes = list(set().union(self.query_graph.nodes(), self.db_graph.nodes()))
        nodes = numpy.array(list_nodes)

        for node in self.query_graph.nodes():
            bitmap = numpy.zeros((len(nodes)), dtype=bool)

            if not self.db_graph.has_node(node):
                self.query_dictionary[node] = self.create_nhindex(node, self.query_graph, nodes, [])
                bitmap = numpy.zeros((len(nodes)), dtype=bool)
                result[node] = (nodes, bitmap)
                continue

            for i in range(0, bitmap.size):
                if nodes[i] in list(self.db_graph.neighbors(node)):
                    bitmap[i] = 1

            self.query_dictionary[node] = self.create_nhindex(node, self.query_graph, nodes,
                                                              list(self.db_graph.neighbors(node)))
            result[node] = (nodes, bitmap)

        return result

    def create_nhindex(self, node, graph, nodes_all, neighbours):
        bitmap = numpy.zeros((len(nodes_all)), dtype=bool)
        for i in range(0, bitmap.size):
            if nodes_all[i] in neighbours:
                bitmap[i] = 1
        return NHIndex.NHIndex(node, graph, nodes_all, bitmap)

    def bitmap_probe(self, query_node, bitmap, n, Sbit, p):
        """
            Function to probe bitmap which extracts only nodes with high probability of matching query node
            :arg query_node:  NHIndex - NHIndex constructed for query node
            :arg bitmap: NHIndex - in general array of neighbours for all nodes which has the same label
            :arg n: int - number of nodes with given label
            :arg Sbit: int - size of neighbours array
            :arg p: double - is the percentage of  neighbors of a query node that can be missing in the match to a database node
            :return Result is the bit vector indicating which nodes satisfy the query
        """

        # the threshold for the number of missing neighbors
        nb_miss = int(math.floor(p * query_node.degree))
        if nb_miss == 0:
            nb_miss = 1
        countSize = int(math.floor(math.log(nb_miss, 2)) + 1.0)
        Count = numpy.zeros((countSize, n), numpy.bool)
        for j in range(0, Sbit):
            if bitmap[j] == 1:
                carries = numpy.bitwise_not(bitmap[j])
                for k in range(0, countSize - 1):
                    temp = numpy.bitwise_and(Count[k], carries)
                    Count[k] = numpy.bitwise_xor(Count[k], carries)
                    carries = temp
                Count[countSize - 1] = numpy.bitwise_or(Count[countSize - 1], carries)
        # returning the nodes with no more than nb_miss neighbours
        result_lt = numpy.zeros(n, numpy.bool)
        result_eq = numpy.full(n, 1, numpy.bool)
        nb_miss_bin = numpy.unpackbits(numpy.array([nb_miss], dtype=numpy.uint8))
        for k in range(countSize, 0):
            if nb_miss_bin[-k - 1] == 1:
                result_lt = numpy.bitwise_or(result_lt, numpy.bitwise_and(result_eq, numpy.bitwise_not(Count[k])))
                result_eq = numpy.bitwise_and(result_eq, Count[k])
            else:
                result_eq = numpy.bitwise_and(result_eq, numpy.bitwise_not(Count[k]))

        result_lt = numpy.bitwise_or(result_lt, result_eq)
        return result_lt

    def grow_match(self, m_imp, query_index_dictionary, graph_index_dictionary):
        """
        :param m_imp: graph containing the matches for the important nodes in query_graph
        :param query_index_dictionary: dictionary containing query nodes as a key with NHIndex for given node as a value
        :param graph_index_dictionary: dictionary containing all query nodes from db_graph as a key with NHIndex for given node as a value
        :return: M contains the node matches for the resulting graph match
        """

        priority_queue = Queue.PriorityQueue()
        M = nx.DiGraph()
        for node in m_imp.nodes():
            quality = self.compute_quality(query_index_dictionary[node], self.db_graph, node)
            priority_queue.put((quality, node))

        while not priority_queue.empty():
            value = priority_queue.get()
            node = value[1]
            M = self.put_node(M, self.query_graph, node)
            self.examine_nodes_near_by(self.query_graph, self.db_graph, query_index_dictionary[node],
                                       node, M, priority_queue)

        return M

    def compute_quality(self, query_node, db_graph, node):
        """

        :param query_node:  NHIndex - NHIndex constructed for query node
        :param db_graph: graph from database
        :param node: node for which quality is indicated
        :return: quality factor for given node
        """

        # actual number of missing neighbours for node
        nb_miss = self.get_missing_neighbours(node)
        # actual number of missing neighbours connections
        nbc_miss = self.get_missing_neighbours_connections(node)
        # fraction of missing neighbours
        fnb = nb_miss / float(query_node.degree)
        # fraction of missing connections
        if query_node.nb_connection == 0:
            fnbc = 0
        else:
            fnbc = nbc_miss / float(query_node.nb_connection)

        if nb_miss == 0:
            w = 2 - fnbc
        else:
            w = 2 - (fnb + fnbc / nb_miss)

        if w == 0:
            return 1

        return 1 / float(w)

    def put_node(self, M, db_graph, node):
        """
        Method for adding matching node to M with included edges
        :param M: contains all the current node matches found so far
        :param db_graph: db_graph
        :param node: node to add
        """
        nodes = M.nodes()
        nodes_list = list(nodes)
        nodes_list.append(node)
        return db_graph.subgraph(nodes_list)

    def examine_nodes_near_by(self, query_graph, db_graph, n_q, n_db, M, priority_queue):
        """
        Method to find new matches for nodes nearby n_q
        :param query_graph: query graph
        :param db_graph: database graph
        :param n_q: node in query graph
        :param n_db: node in database graph
        :param M: contains all the current node matches found so far
        :param priority_queue: all candidate node matches to be examined
        """
        # immediate neighbours of n_q that has no matches in M
        N_B1_q = []
        # neighbours of n_q two hops away
        N_B2_q = []
        # immediate neighbors of n_db that have no matches in either M or priority queue
        N_B1_db = []
        # nodes two hops away from n_db that have no matches in either M or priority_queue
        N_B2_db = []

        for neighbour in query_graph.neighbors(n_q.label):
            if not M.has_node(neighbour):
                N_B1_q.append(neighbour)

            for two_hop_neighbour in query_graph.neighbors(neighbour):
                if not M.has_node(two_hop_neighbour):
                    N_B2_q.append(two_hop_neighbour)

        for neighbour in db_graph.neighbors(n_db):
            if not M.has_node(neighbour) and not any(neighbour == item[1] for item in priority_queue.queue):
                N_B1_db.append(neighbour)

            for two_hop_neighbour in db_graph.neighbors(neighbour):
                if not M.has_node(two_hop_neighbour) and not any(
                        two_hop_neighbour == item[1] for item in priority_queue.queue):
                    N_B2_db.append(two_hop_neighbour)

            self.match_nodes(query_graph, db_graph, N_B1_q, N_B1_db, M, priority_queue)
            self.match_nodes(query_graph, db_graph, N_B1_q, N_B2_db, M, priority_queue)
            self.match_nodes(query_graph, db_graph, N_B2_q, N_B1_db, M, priority_queue)

    def match_nodes(self, query_graph, db_graph, S_q, S_db, M, priority_queue):
        """

        :param query_graph: query graph
        :param db_graph: database graph
        :param S_q: set of nodes in query graph
        :param S_db: set of nodes in db_graph
        :param M: contains all the current node matches found so far
        :param priority_queue: all candidate node matches to be examined
        """

        for node in S_q:
            if node in S_db:
                node_db = node
                missing_neighbours = self.get_missing_neighbours(node)
                number_of_neighbours = len(list(nx.neighbors(query_graph, node)))
                if number_of_neighbours > 0:
                    percent_of_missing_neighbours = float(missing_neighbours) / float(number_of_neighbours)
                    if percent_of_missing_neighbours > self.p:
                        continue

                missing_connections = self.get_missing_neighbours_connections(node)
                subgraph = self.db_graph.subgraph(self.db_graph.neighbors(node))
                nb_connections = len(subgraph.edges())

                if nb_connections > 0:
                    percent_of_missing_connections = float(missing_connections) / float(nb_connections)
                    if percent_of_missing_connections > self.p:
                        continue
            else:
                continue

            if not any(node == item[1] for item in priority_queue.queue):
                priority = self.compute_quality(self.query_dictionary[node], self.db_graph, node_db)
                priority_queue.put((priority, node))
                S_db.remove(node_db)

    def get_missing_neighbours(self, node):
        count = 0
        neighbours = self.query_graph.neighbors(node)
        for neighbour in neighbours:
            if neighbour not in self.db_graph.nodes():
                count += 1
            elif neighbour not in self.db_graph.neighbors(node):
                count += 1
            else:
                if self.dict[neighbour] != self.dict[node]:
                    count += 1
        return count


    def get_missing_neighbours_connections(self, node):
        count = 0
        neighbours = list(self.query_graph.neighbors(node))
        subgraph_query = self.query_graph.subgraph(neighbours)
        subgraph_db = self.db_graph.subgraph(neighbours)
        for edge in subgraph_query.edges():
            if not subgraph_db.has_edge(edge[0], edge[1]):
                count += 1

        return count

    def get_important_nodes(self, write_to_file = False, out_dir = None):

        dict = nx.harmonic_centrality(self.db_graph)

        sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
        if write_to_file is True:
            file_name = "{0}/salon24_eigenvector_centrality_{1}".format(out_dir, self.index)
            with open(file_name, 'w') as file:
                file.write(pickle.dumps(sorted_dict)) # use `pickle.loads` to do the reverse

        number_of_items_to_get = int(math.floor(len(sorted_dict) * self.importance_threshold))

        undirected = self.db_graph.to_undirected()


        try:
            independent_set = nx.maximal_independent_set(undirected)
        except nx.NetworkXUnfeasible:
            independent_set = []

        result = []

        for item in sorted_dict[:number_of_items_to_get]:
            if item[0] in independent_set:
                result.append((item[0], item[1]))

        if len(result) == 0:
            return sorted_dict[:number_of_items_to_get]

        # lista tupli
        return result

    def set_disjoint_set_for_graph(self):
        disjoint_set = DisjointSet(self.db_graph.nodes())
        for edge in self.db_graph.edges():
            disjoint_set.union(edge[0],edge[1])
        set = disjoint_set.get()

        dict = {}
        for item in set:
            for elem in item:
                dict[elem] = set.index(item)

        return disjoint_set, dict