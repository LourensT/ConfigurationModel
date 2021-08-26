
import numpy as np

import matplotlib.pyplot as plt

from CM import CM


n = 1001
tau = 3.5

'''
determinstic degree sequence (according to powerlaw distribution in #6.2.21 form vol1
'''
def sampleDegreeSequence(size):

    weights = np.zeros(size)

    for i in range(size):
        w = int((((i+1)/size)**(-1/(tau -1))))
        weights[i] = w

    return weights


degree_sequence = sampleDegreeSequence(n)

print(sum(degree_sequence))

graph = CM(degree_sequence)


distr = graph.DegreeDistribrution(tail=True)
distrBiased = graph.SizeBiasedDegreeDistribution(tail=True)
friendBiased = graph.RandomFriendDegreeDistribution(tail=True)
# plot degree distribution
plt.scatter(x=distr.keys(), y=distr.values(), color='red')
print(max(distr.keys()))
plt.scatter(x=distrBiased.keys(), y=distrBiased.values(), color='green')
print(max(distrBiased.keys()))
plt.scatter(x=friendBiased.keys(), y=friendBiased.values(), color='blue')
print(max(friendBiased.keys()))
plt.legend(["Normal Degree Distribution", "size Biased Degree Distribution", "Friend"])
plt.title("Tail Distributions of degrees, tau=3.5")
plt.show()

