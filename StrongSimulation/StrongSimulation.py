import networkx as nx


class StrongSimulation:

    def __init__(self, query_graph, graph, query_diameter):
        self.query_graph = query_graph
        self.query_diameter = query_diameter
        self.graph = graph

    def dual_sim(self, ball):
        sim = {}
        for vertex in self.query_graph.nodes():
            if ball.has_node(vertex) and self.graph.has_node(vertex):
                sim[vertex] = [vertex]

        flag = True

        while flag is True:
            flag = False
            for edge in self.query_graph.edges():
                v = edge[0]
                v_prim = edge[1]
                if v in sim and v_prim in sim:
                    for u in sim[v]:
                        for u_prim in sim[v_prim]:
                            if ball.has_edge(u, u_prim) is False:
                                sim[v].remove(u)
                                flag = True

        Sw = []
        for vertex in self.query_graph.nodes():
            if not vertex in sim or len(sim[vertex]) == 0:
                return []
            Sw.append((vertex, sim[vertex][0]))

        return Sw

    def match(self):
        result = []

        for vertex in self.graph.nodes():
            ball = self.get_ball(vertex)
            Sw = self.dual_sim(ball)
            Gs = self.extract_max_pg(ball, Sw, vertex)
            if len(Gs.nodes()) > 0:
                result.append(Gs)

        return result

    def get_ball(self, vertex):
        undirected_graph = self.graph.to_undirected()
        bfs_tree = nx.bfs_tree(undirected_graph, vertex)  # returns DiGraph
        subgraph_nodes = []
        undirected_bfs_tree = bfs_tree.to_undirected()
        shortest_paths = nx.shortest_path_length(undirected_bfs_tree, vertex);

        for v in shortest_paths:
            if shortest_paths[v] <= self.query_diameter:
                subgraph_nodes.append(v)

        ball = self.graph.subgraph(subgraph_nodes)

        return ball

    def extract_max_pg(self, ball, Sw, vertex):
        if (vertex, vertex) not in Sw:
            return nx.Graph()

        vertex_list = []

        for t in Sw:
            vertex_list.append(t[1])

        return ball.subgraph(vertex_list)
