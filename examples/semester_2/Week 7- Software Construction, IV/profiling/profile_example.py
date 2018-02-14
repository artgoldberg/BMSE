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

    def __init__(self, args):
        self.args = args

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(description="Example profiling code")
        parser.add_argument('graph_size', type=int, help="Graph size")
        parser.add_argument('sub_graph_size', type=int, help="Subgraph size")
        parser.add_argument('--profile', action='store_true', help="Profile the code")
        args = parser.parse_args()
        if not 2*args.sub_graph_size<args.graph_size:
            sys.stderr.write("Error: 2*sub_graph_size < graph_size must hold\n")
            sys.exit()
        return args

    def shortest_path(self, G):
        p = nx.algorithms.shortest_paths.generic.shortest_path(
            G, source=choice(list(G.nodes())), target=choice(list(G.nodes())))
        print("{} node path".format(len(p)))

    def subgraph_match(self):
        complete_subgraph = nx.complete_graph(self.args.graph_size)
        gm = GraphMatcher(self.complete_graph, complete_subgraph)
        is_isomorphic = gm.subgraph_is_isomorphic()
        print("Is isomorphic?: {}".format(is_isomorphic))

    def run(self):
        # Shortest path
        self.balanced_tree = nx.balanced_tree(2, math.floor(math.log2(self.args.graph_size)))
        self.shortest_path(self.balanced_tree)
        
        # subgraph isomorphism
        self.complete_graph = nx.complete_graph(self.args.graph_size)
        self.subgraph_match()

# example run
# python profile_example.py --profile 500 120
if __name__ == '__main__':

    args = Example.parse_args()
    if args.profile:
        OUT_FILE = 'stats.out'
        cProfile.run('Example(args).run()', OUT_FILE)
        profile = pstats.Stats(OUT_FILE)
        profile.strip_dirs().sort_stats('cumulative').print_stats(10)
    else:
        Example(args).run()
