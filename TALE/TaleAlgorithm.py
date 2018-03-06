import logging
import math
import copy
import numpy


class Tale:

    def __init__(self, query_graph):
        FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.INFO)
        self.query_graph = query_graph

    def run_algorithm(self):
        logging.info("TALE algorithm run method started")
        pass




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


        #the threshold for the number of missing neighbors
        nb_miss = math.floor(p * query_node.degree)
        countSize = math.floor(math.log(nb_miss, 2)) + 1.0
        Count = numpy.zeros((countSize, n), numpy.bool)
        for j in range(0, Sbit):
            if query_node.nb_array[j] == 1:
                carries = numpy.bitwise_not(bitmap[:,j])
                for k in range(0, countSize - 1):
                    temp = numpy.biwise_and(Count[k], carries)
                    Count[k] = numpy.bitwise_xor(Count[k], carries)
                    carries = temp
                Count[countSize] = numpy.bitwise_or(Count[countSize], carries)
        #returning the nodes with no more than nb_miss neighbours
        result_lt = numpy.zeros(n, numpy.bool)
        result_eq = numpy.full(n, 1, numpy.bool)
        nb_miss_bin = numpy.unpackbits(numpy.array([nb_miss]))
        for k in range(countSize, 0):
            if nb_miss_bin[-k - 1] == 1:
                result_lt = numpy.bitwise_or(result_lt, numpy.bitwise_and(result_eq, numpy.bitwise_not(Count[k])))
                result_eq = numpy.bitwise_and(result_eq, Count[k])
            else:
                result_eq = numpy.bitwise_and(result_eq, numpy.bitwise_not(Count[k]))

        result_lt = numpy.bitwise_or(result_lt, result_eq)
        return result_lt








