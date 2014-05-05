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

def WriteToNauty(graph):
  nodes = sorted(graph.keys())
  nauty = open('/tmp/nauty', 'w')
  nauty.write('n=%d g\n' % len(nodes))
  for node in nodes:
    nauty.write('%s : %s\n' % (node, ' '.join(map(str, sorted(graph[node].keys()))) + ';'))
  nauty.write('-a-mcx\n')
  nauty.write('b\n')
  nauty.close()
def GetCanonical(graph):
  WriteToNauty(graph)
  cmd = '/projects/grail/marcotcr/johan/nauty25r9/dreadnaut < /tmp/nauty | grep :'
  can = os.popen(cmd).read()
  return can

def MakeSubGraph(graph, nodes):
  new_graph = collections.defaultdict(lambda:collections.defaultdict(lambda: False))
  for i in range(len(nodes)):
    node1 = nodes[i]
    new_graph[i]
    for j in range(i + 1, len(nodes)): 
      node2 = nodes[j]
      if node2 in graph[node1]:
        new_graph[i][j] = True
        new_graph[j][i] = True
  return new_graph
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
    new_graph = MakeSubGraph(graph, nodes)
    rep = GetCanonical(new_graph)
    rep = re.sub('\s', '', rep)
    counts[rep] += 1
  for x,y in counts.iteritems():
    print x,y


if __name__ == '__main__':
  main()
