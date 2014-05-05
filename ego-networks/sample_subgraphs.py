#!/usr/bin/python
"""
Randomly sample 3-node or 4-node subgraphs from a given graph, n times. Outputs
a feature vector containing the normalized counts of each of the possible
configurations.
"""
import sys
import getopt
import collections
import os
import re
import numpy as np

def Usage():
  print '%s' % sys.argv[0]
  print 'Options:'
  print '-e (required): edge file. (.edges)'
  print '-o (required): output file'
  print '-n (required): number of times to sample'
  print '-3 (optional): do size-3 subgraphs. Default is size 4'
  print 'Example usage:'
  print '%s -e twitter/100318079.edges -o 100318079.counts -n 1000' % sys.argv[0]
  quit()

def count_3(count_vector, graph, nodes):
  """I'm assuming undirected here"""
  edges = 0
  if nodes[1] in graph[nodes[0]]:
    edges += 1
    
  if nodes[2] in graph[nodes[0]]:
    edges += 1

  if nodes[2] in graph[nodes[1]]:
    edges += 1
  count_vector[edges] += 1

mapping = {'0000':0, '0011':1, '0112' :2, '0222':3, '1111': 4, '1113':5, 
'1122':6, '1223':7, '2222': 8, '2233':9, '3333':10}
def count_4(count_vector, graph, nodes):
  """I'm assuming undirected here"""
  node_degrees = np.zeros(4, dtype=int)
  for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
      if nodes[j] in graph[nodes[i]]:
        node_degrees[i] += 1
        node_degrees[j] += 1
  degrees = ''.join(sorted(''.join(map(str,node_degrees))))
  count_vector[mapping[degrees]] += 1 


def generate_count_vector(subgraph_size):
  if subgraph_size == 3:
    # no edges:0 edges,  1 edge, 2 edges, 3 edges
    return np.zeros(4)
  if subgraph_size == 4:
    # node degrees:
    # 0 0 0 0 y1
    # 0 0 1 1 y2
    # 0 1 1 2 y4
    # 0 2 2 2 y5
    # 1 1 1 1 y3
    # 1 1 1 3 y7
    # 1 1 2 2 y6
    # 1 2 2 3 y8
    # 2 2 2 2 y9
    # 2 2 3 3 y10
    # 3 3 3 3 y11
    return np.zeros(11)

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "e:o:n:3")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  edge_file = None
  n_samples = None
  subgraph_size = 4
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-e':
      edge_file = value
    elif option == '-n':
      n_samples = int(value)
    elif option == '-3':
      subgraph_size = 3
    else:
      assert False, "Option %s not available" % option
  if not edge_file or not n_samples:
    Usage()
  try:
    target_node = re.search('(\d+).edges', edge_file).group(1)
  except:
    Usage()
  all_nodes = set()
  graph = collections.defaultdict(lambda:collections.defaultdict(lambda: False))
  for line in open(edge_file):
    node1, node2 = line.strip().split()
    all_nodes.add(node1)
    all_nodes.add(node2)
    graph[node1][node2] = True
  for node in all_nodes:
    graph[target_node][node] = True

  flat_nodes = list(all_nodes)
  count_vector = generate_count_vector(subgraph_size)
  for i in range(n_samples):
    nodes = np.random.choice(flat_nodes, subgraph_size, replace=False)
    if subgraph_size == 3:
      count_3(count_vector, graph, nodes)
    if subgraph_size == 4:
      count_4(count_vector, graph, nodes)

  print count_vector / n_samples


if __name__ == '__main__':
  main()
