""" Test DAG
:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2020-07-08
:Copyright: 2020, Karr Lab
:License: MIT
"""

import unittest

from wc_sim.utils.dag import DAG


class TestDAG(unittest.TestCase):

    def test(self):
        dag = DAG()
        dag.add_node(1)
        self.assertIn(1, dag.nodes())
        dag.rm_node(1)
        self.assertNotIn(1, dag.nodes())
        dag.add_edge(1, 2)
        self.assertIn((1, 2), dag.edges())
        dag.rm_edge(1, 2)
        self.assertNotIn((1, 2), dag.edges())
        dag.add_edge(1, 2)
        dag.add_edge(1, 3)
        dag.add_edge(2, 4)
        dag.add_edge(3, 4)
        self.assertEqual({1, 2, 3, 4}, set(dag.dfs(1)))
        self.assertEqual({2, 4}, set(dag.dfs(2)))
        self.assertEqual({4}, set(dag.dfs(4)))
