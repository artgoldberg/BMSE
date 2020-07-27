""" Fast, compact DAG for analyzing expression dependencies

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2020-07-08
:Copyright: 2020, Karr Lab
:License: MIT
"""

class DAG(object):
    """ Fast, compact DAG for analyzing expression dependencies

    `networkx` is not usable because its traversal methods use too much RAM.
    `DAG` represents a DAG as an adjacency list in a Python `dict`.
    """

    def __init__(self):
        self.dag = {}

    def add_node(self, node):
        """ Add a node
        """
        if node in self.dag:
            raise ValueError('node in self.dag')
        self.dag[node] = set()

    def rm_node(self, node):
        """ Remove a node
        """
        if node not in self.dag:
            raise ValueError('node not in self.dag')
        del self.dag[node]

    def nodes(self):
        """ Get the nodes
        """
        return self.dag.keys()

    def add_edge(self, source, dest):
        """ Add an edge
        """
        if source not in self.dag:
            self.add_node(source)
        self.dag[source].add(dest)

    def rm_edge(self, source, dest):
        """ Remove an edge
        """
        if source not in self.dag:
            raise ValueError('source not in self.dag')
        self.dag[source].discard(dest)

    def edges(self):
        """ Provide all edges
        """
        edges = []
        for src, dests in self.dag.items():
            edges.extend([(src, d) for d in dests])
        return edges

    def dfs(self, source):
        """ Generate a depth-first search
        """
        if source not in self.dag:
            yield source
        else:
            visited = set()
            visited.add(source)
            to_visit = list()   # a list of iterators over nodes
            to_visit.append(self.dag[source])
            yield source
            while to_visit:
                nodes = to_visit.pop()
                for node in nodes:
                    if node not in visited:
                        yield node
                        visited.add(node)
                        if node in self.dag:
                            to_visit.append(self.dag[node])
