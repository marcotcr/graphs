#!/usr/bin/env python
import sys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as cl
#import re
import math
#import random
import numpy

from itertools import groupby
from operator import itemgetter


nodecounter=0
s = (line.rstrip().split() for line in sys.stdin)
for ((degree, userid), row) in groupby(s, itemgetter(0,1)):
  nodecounter += 1
  G = nx.Graph()

  nodes = {}
  for (friend1, friend2) in row:
    G.add_edge(friend1, friend2,)
    #G.add_node(friend1, age = int(age1), gender = gender1)
    #G.add_node(friend2, age = int(age2), gender = gender2)

  plt.figure(1, figsize=(14,4))
  plt.figure(1).clear()

  G_components = nx.connected_component_subgraphs(G)
  numCCs = len(G_components)

  p=int(math.ceil(math.sqrt(numCCs)))
  p=4
  q=1
  plotnodesize=30
  extras=0

  for i in range(1,min(numCCs,p*q)+1):
    G_plot = G_components[i-1]
    plt.subplot(q,p,i)

    if (i == p*q):
      for r in range(p*q+1,numCCs+1):
        G_plot=nx.union(G_plot,G_components[r-1])

    pos=nx.spring_layout(G_plot)
    #alphas = [str(min(1.0, (G.node[x]['age']-13)/50.0)) for x in G.node]
    # modify this line to potentially vary colors
    colors = ['red' for x in G.node]
    colorsToPlot = []
    #for i in xrange(len(alphas)):
    #    colorsToPlot[i] = cl.ColorConverter.to_rgba(
    #            cl.ColorConverter.to_rgb(colors[i]), alphas[i])
    nx.draw(G_plot,pos, node_color = colors,
      edge_color='black', node_size=plotnodesize, with_labels=False)

  plt.savefig("plots/" + str(degree) + "_plot" + str(nodecounter) + ".png")

