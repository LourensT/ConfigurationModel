# Configuration Model
import networkx as nx

from typing import List

import numpy as np

import matplotlib.pyplot as plt


class CM:


    '''
    Generates a Configuration Model mulitgraph based on the given degree sequence

    @param degree_sequence: list of number of degrees, length determines number of vertices
                        - assumes no 0s in degree_sequence
    '''
    def __init__(self, degree_sequence: List[int]):

        for d in degree_sequence:
            assert d > 0, "non-positive degree"

        # shuffle the degree distribution to get random order
        np.random.shuffle(degree_sequence)

        print(degree_sequence)

        self.G = nx.MultiGraph()
        self.n = len(degree_sequence)

        # number of half-edges
        half_edges = {}

        # names of vertices runs from 0 to n-1
        for i in range(self.n):
            self.G.add_node(i)
            half_edges[i] = degree_sequence[i]



        while len(half_edges) > 0:
            print(half_edges)
            keys_left = list(half_edges.keys())
            v = keys_left[0]
            keys_left = keys_left[1:]

            v_has_half_edges_left = True
            while v_has_half_edges_left:
                if len(keys_left) == 0:
                    self.G.add_edge(v, v)
                    half_edges[v] -= 2
                else:
                    u = np.random.choice(keys_left)
                    self.G.add_edge(v, u)

                    # decrease half edges
                    half_edges[v] -= 1
                    half_edges[u] -= 1
                    
                    if half_edges[u] == 0:
                        del half_edges[u]
                        keys_left.remove(u)

                if half_edges[v] <= 0:
                    del half_edges[v]
                    v_has_half_edges_left = False
                    

    def draw(self):
        nx.draw(self.G)
        plt.show()



if __name__ == "__main__":
    while True:
        cm = CM([1, 1, 2, 1, 2, 3, 4, 5, 6, 3, 4, 5, 6])
        cm.draw()
            


