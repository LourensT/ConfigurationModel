# Configuration Model
import networkx as nx

from typing import List

import numpy as np

import matplotlib.pyplot as plt

from DegreeDistributions.DegreeDistributions import *

import random

class CM:


    '''
    Generates a Configuration Model mulitgraph based on the given degree sequence

    @param degree_sequence: list of number of degrees, length determines number of vertices
                        - assumes no 0s in degree_sequence
    '''
    def __init__(self, degree_sequence: List[int]):

        self._checkIfValidDegreeSequence(degree_sequence)

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
        assert not(0 in degree_sequence), "degree sequence contains 0"
        assert (sum(degree_sequence) % 2 == 0), "degree sequence is not even"

                    
    def DegreeDistribrution(self, tail=True):
        return DegreeDistribution(self.G, tail=tail)

    def RandomFriendDegreeDistribution(self, tail=True):
        return RandomFriendDegreeDistribution(self.G, tail=tail)

    def SizeBiasedDegreeDistribution(self, tail=True):
        return SizeBiasedDegreeDistribution(self.G, tail=tail)

    def draw(self):
        nx.draw(self.G)
        plt.show()

    def AreThereParallelsEdges(self):
        for n in self.G.nodes:
            if len(self.G.adj[n]) < 3:
                return True
        
        return False

        '''
    Returns distribution of typical distance:
    - the length of the shortest path between two randomly drawn nodes, given that they are connected

    @param sample: The number of randomly drawn 

    '''
    def typicalDistanceDistribution(self, sample=-1):

        all_shortest_paths = []
        if sample == -1:
            #dictionary of dictionaries dict[source][target] = path
            for source, destinations in nx.algorithms.shortest_path(self.G).items():
                for destination, path in destinations.items():
                    all_shortest_paths.append(path)
        else:
            for i in range(sample):
                found_path = False
                while not found_path:
                    source = random.choice(list(self.G.nodes))
                    target = random.choice(list(self.G.nodes))

                    try:
                        all_shortest_paths.append(nx.algorithms.shortest_path(self.G, source, target))
                        found_path = True
                    except nx.exception.NetworkXNoPath:
                        found_path = False

                    

        # calculate pmf
        pmf = {}
        numberOfPaths = 0 #if sample > 0, then this will end up being equal to sample
        for path in all_shortest_paths:
            if (len(path)-1) in pmf:
                pmf[len(path)-1] += 1
            else: 
                pmf[len(path)-1] = 1
            numberOfPaths += 1

        print(numberOfPaths)

        #normalize the histogram (paths currently double counted)
        for key in pmf.keys():
            pmf[key] = pmf[key] / numberOfPaths

        assert abs(sum([v for v in pmf.values()]) - 1) < 0.001, "pmf does not sum to one!!"

        return pmf

if __name__ == "__main__":
    # generate random CM with degr_sequence
    #degr_sequence = np.random.choice([i for i in range(1, 10)], size=50)
    degr_sequence = [3 for _ in range(50)]
    print("degree sequence with sum of", sum(degr_sequence))
    cm = CM(degr_sequence)
    print("Are There Parallels Edges: ", cm.AreThereParallelsEdges())
    cm.draw()
