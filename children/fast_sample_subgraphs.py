#!/usr/bin/python
"""
Randomly sample subgraphs from a given graph, n times.
"""
import sys
import getopt
import random
import collections
import os
import re
import numpy as np

def Usage():
  print '%s' % sys.argv[0]
  print 'Options:'
  print '-e (required): edge file. (.edges)'
  print '-n (required): number of times to sample'
  print '-s (required): subgraph size'
  print 'Example usage:'
  print 'python sample_subgraphs.py -e ../../gplus/100637660947564674695.edges -n 1 -s 5' 
  quit()

def DegreeDistribution(graph):
  # This only works for graphs up to size 10
  out = ''
  for x in graph:
    out += '%d' % len(graph[x])
  return 'DegreeDistribution:'+''.join(sorted(out))

def LongestShortestPathDistribution(graph):
  nodes = set(graph.keys())
  return 'LSP:'+ ''.join(map(str,sorted([LongestShortestPath(graph, node) for node in nodes])))

def LongestShortestPath(graph, node):
  Q = [node]
  #distances = {x:9 for x in graph.keys()}
  distances = dict([(x, 9) for x in graph.keys()])
  distances[node] = 0
  visited = set([node])
  while Q:
    x = Q.pop(0)
    for y in graph[x]:
      if y not in visited:
        distances[y] = distances[x] + 1
        Q.append(y)
        visited.add(y)
  return max(distances.values())

def ConnectedComponents(graph):
  """Sizes of connected components"""
  nodes = set(graph.keys())
  ccs = 0
  size_ccs = []
  while nodes:
    size_cc = 0
    Q = [nodes.pop()]
    while Q:
      x = Q.pop(0)
      size_cc += 1
      for y in graph[x]:
        if y in nodes:
          nodes.remove(y)
          Q.append(y)
    size_ccs.append(size_cc)  
  return 'CCS:'+ ''.join(map(str,sorted(size_ccs)))

def Bipartite(graph):
  """Sizes of connected components"""
  nodes = set(graph.keys())
  colors = collections.defaultdict(lambda: 'R')
  while nodes:
    Q = [nodes.pop()]
    colors[Q[0]] = 'R'
    while Q:
      x = Q.pop(0)
      for y in graph[x]:
        if y in colors:
          if colors[y] == colors[x]:
            return 'Bipartite:F'
        else:
          colors[y] = 'B' if colors[x] == 'R' else 'R'
        if y in nodes:
          nodes.remove(y)
          Q.append(y)
  return 'Bipartite:T'




def MakeSubGraph(graph, nodes):
  new_graph = collections.defaultdict(lambda:collections.defaultdict(lambda: False))
  complement = collections.defaultdict(lambda:collections.defaultdict(lambda: False))
  for i in range(len(nodes)):
    node1 = nodes[i]
    new_graph[i]
    complement[i]
    for j in range(i + 1, len(nodes)): 
      node2 = nodes[j]
      if node2 in graph[node1]:
        new_graph[i][j] = True
        new_graph[j][i] = True
      else:
        complement[i][j] = True
        complement[j][i] = True
  return new_graph, complement

def FeatureSwitch(graph, feature):
  #if feature == 'number_of_edges':
  #  return NumberOfEdges(graph)
  if feature == 'degree_distribution':
    return DegreeDistribution(graph)
  if feature == 'ccs':
    return ConnectedComponents(graph)
  if feature == 'longest_shortest_path':
    return LongestShortestPathDistribution(graph)
  #if feature == 'diameter':
  #  return Diameter(graph)
  if feature == 'bipartite':
    return Bipartite(graph)
  #if feature == 'mst':
  #  return MST(graph)
  #if feature == 'nodes_at':
  #  return_ = ''
  #  for i in range(10):
  #    return_ += NodesAtDistanceKDistribution(graph, i) + '-'
  #  return return_


def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "e:s:n:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  edge_file = None
  n_samples = None
  subgraph_size = None
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-e':
      edge_file = value
    elif option == '-n':
      n_samples = int(value)
    elif option == '-s':
      subgraph_size = int(value)
    else:
      assert False, "Option %s not available" % option
  if not edge_file or not n_samples or not subgraph_size:
    Usage()
  all_nodes = set()
  graph = collections.defaultdict(lambda:collections.defaultdict(lambda: False))
  node_id = {}
  features = ['degree_distribution', 'ccs', 'bipartite', 'longest_shortest_path']
  current_id = 1
  # This assumes an undirected graph.
  for line in open(edge_file):
    node1, node2 = line.strip().split()
    if node1 not in node_id:
      node_id[node1] = str(current_id)
      current_id += 1
    if node2 not in node_id:
      node_id[node2] = str(current_id)
      current_id += 1
    node1 = node_id[node1]
    node2 = node_id[node2]
    all_nodes.add(node1)
    all_nodes.add(node2)
    graph[node1][node2] = True
    graph[node2][node1] = True

  flat_nodes = list(all_nodes)
  # count_vector = generate_count_vector(subgraph_size)
  counts = collections.defaultdict(lambda:0.0)
  for i in range(n_samples):
    # if i % 100 == 0:
    #   print i
    nodes = random.sample(flat_nodes, subgraph_size)
    new_graph, complement = MakeSubGraph(graph, nodes)
    rep = ''
    for feature in features:
      rep += '%s-' % FeatureSwitch(new_graph, feature)
    for feature in features:
      rep += 'Complement%s-' % FeatureSwitch(complement, feature)
    rep = rep.strip('-')
    counts[rep] += 1

  for x,y in counts.iteritems():
    print x,y


if __name__ == '__main__':
  main()
