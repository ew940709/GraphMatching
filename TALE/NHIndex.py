class NHIndex:

    def __init__(self, label, graph, neighbours_array, bitmap):
        self.label = label
        self.graph = graph
        self.degree = graph.degree(label)
        self.nb_connection = self.get_nb_connection()
        self.nb_array = neighbours_array
        self.bitmap = bitmap

    def get_nb_connection(self):
        subgraph = self.graph.subgraph(self.graph.neighbors(self.label))
        return len(subgraph.edges())


