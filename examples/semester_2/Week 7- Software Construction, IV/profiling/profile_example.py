"""
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2018-02-14
:Copyright: 2018, Arthur Goldberg
"""
import sys
import math
import argparse
import cProfile
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from random import choice
import pstats

class Example(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description="Example profiling code")
        parser.add_argument('graph_size', type=int, help="Graph size")
        parser.add_argument('sub_graph_size', type=int, help="Subgraph size")
        self.args = parser.parse_args()
        if not 2*self.args.sub_graph_size<self.args.graph_size:
            sys.stderr.write("Error: 2*sub_graph_size < graph_size must hold\n")
            sys.exit()

    def shortest_path(self, G):
        p = nx.algorithms.shortest_paths.generic.shortest_path(
            G, source=choice(list(G.nodes())), target=choice(list(G.nodes())))
        print("{} node path".format(len(p)))

    def subgraph_match(self):
        complete_subgraph = nx.complete_graph(self.args.graph_size)
        gm = GraphMatcher(self.complete_graph, complete_subgraph)
        is_isomorphic = gm.subgraph_is_isomorphic()
        print("{} is isomorphic".format(is_isomorphic))

    def run(self):
        self.balanced_tree = nx.balanced_tree(2, math.floor(math.log2(self.args.graph_size)))
        self.shortest_path(self.balanced_tree)
        
        self.complete_graph = nx.complete_graph(self.args.graph_size)
        self.subgraph_match()
            
if __name__ == '__main__':
    OUT_FILE = 'stats.out'
    cProfile.run('Example().run()', OUT_FILE)
    profile = pstats.Stats(OUT_FILE)
    profile.strip_dirs().sort_stats('cumulative').print_stats(10)
