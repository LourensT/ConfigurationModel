# Configuration Model
import networkx as nx

from typing import List

import numpy as np

import matplotlib.pyplot as plt

from DegreeDistributions.DegreeDistributions import *

class CM:


    '''
    Generates a Configuration Model mulitgraph based on the given degree sequence

    @param degree_sequence: list of number of degrees, length determines number of vertices
                        - assumes no 0s in degree_sequence
    '''
    def __init__(self, degree_sequence: List[int]):

        self._checkIfValidDegreeSequence(degr_sequence)

        # shuffle the degree distribution to get random order
        np.random.shuffle(degree_sequence)

        self.G = nx.MultiGraph()
        self.n = len(degree_sequence)

        # number of half-edges
        half_edges = {}

        # names of vertices runs from 0 to n-1
        for i in range(self.n):
            self.G.add_node(i)
            half_edges[i] = degree_sequence[i]

        # generate CM by following steps
        # - select next vertex (v) which still has unfilled half_edges
        # - pick another random other vertex (u) and connect it
        #       - if there are none, self-loops are added to v

        while len(half_edges) > 0:
            keys_left = list(half_edges.keys())
            v = keys_left[0]
            keys_left = keys_left[1:]

            v_has_half_edges_left = True
            while v_has_half_edges_left:
                # self loops to deal with remaining
                if len(keys_left) == 0:
                    self.G.add_edge(v, v)
                    half_edges[v] -= 2
                else:
                    u = np.random.choice(keys_left)
                    self.G.add_edge(v, u)

                    # decrease half edges
                    half_edges[v] -= 1
                    half_edges[u] -= 1
                    
                    # check if (u) still has half_edges left, otherwise remove
                    if half_edges[u] == 0:
                        del half_edges[u]
                        keys_left.remove(u)

                # check if v still has half_edges, otherwise remove
                if half_edges[v] == 0:
                    del half_edges[v]
                    v_has_half_edges_left = False
                # this case should not happen if the sum of degr_sequence is even
                elif half_edges[v] == -1:
                    raise ValueError("-1 for last degree, meaning the degree sequence did not sum even.")


    def _checkIfValidDegreeSequence(self, degree_sequence):
        assert not(0 in degr_sequence), "degree sequence contains 0"
        assert (sum(degr_sequence) % 2 == 0), "degree sequence is not even"

                    
    def DegreeDistribrution(self, tail=True):
        return DegreeDistribution(self.G, tail=tail)

    def RandomFriendDegreeDistribution(self, tail=True):
        return RandomFriendDegreeDistribution(self.G, tail=tail)

    def SizeBiasedDegreeDistribution(self, tail=True):
        return SizeBiasedDegreeDistribution(self.G, tail=tail)

    def draw(self):
        nx.draw(self.G)
        plt.show()



if __name__ == "__main__":
    # generate random CM with degr_sequence
    degr_sequence = np.random.choice([i for i in range(1, 10)], size=50)
    print("degree sequence with sum of", sum(degr_sequence))
    cm = CM(degr_sequence)
    cm.draw()
            


