import simplejson as json
import networkx as nx


def save(G, fname):
    data = nx.node_link_data(G)
    json.dump(data, open(fname, 'w'), indent=2)


def load(fname):
    data = json.load(open(fname))
    return nx.node_link_graph(data, directed=True)
