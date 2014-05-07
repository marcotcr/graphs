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
  print '-d (required): dataset folder'
  print '-n (required): number of times to sample'
  print '-s (required): subgraph size'
  print '-g (required): node feature file'
  print '-l (required): output label file'
  print '-o (required): output data file'
  print 'Example usage:'
  print 'python construct_feature_vectors.py -g nodes_day1 -d biego/ -n 1 -s 5 -l labels -o data' 
  quit()

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "d:s:n:l:o:g:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  dataset_folder = None
  n_samples = None
  subgraph_size = None
  labels = None
  output = None
  node_feature_file = None
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-d':
      dataset_folder = value
    elif option == '-n':
      n_samples = int(value)
    elif option == '-s':
      subgraph_size = int(value)
    elif option == '-g':
      node_feature_file = value 
    elif option == '-l':
      labels = open(value, 'w')
    elif option == '-o':
      output = value 
    else:
      assert False, "Option %s not available" % option
  if not dataset_folder or not n_samples or not subgraph_size or not labels or not output or not node_feature_file:
    Usage()
  
  possible_subgraphs = {3: 4, 4: 11, 5: 34, 6: 156, 7: 1044, 8: 12346, 9: 274668, 10: 12005168}
  k = possible_subgraphs[subgraph_size]
  current_feat = 0
  feat_id = {}
  data = []
  node_gender = {}
  for line in open(node_feature_file):
    node, gender = line.split()[0], line.strip().split()[2]
    if gender == 'M' or gender == 'F':
      node_gender[node] = gender

  graphs = [re.sub('.edges', '', re.sub('%s/' % dataset_folder, '', x.strip())) for x in os.popen('ls %s/*.edges' % dataset_folder).readlines()]
  print 'Total:', len(graphs)
  for graph in graphs:
    node1, node2 = graph.split('-')
    gender = ''.join(sorted('%s%s' % (node_gender[node1], node_gender[node2])))
    edge_file = '%s/%s.edges' % (dataset_folder, graph)
    labels.write('%s\n' % gender)
    features = np.zeros(k) 
    cmd = 'python fast_sample_subgraphs.py -e %s -n %d -s %d' % (edge_file, n_samples, subgraph_size)
    #cmd = 'python sample_subgraphs.py -e %s -n %d -s %d' % (edge_file, n_samples, subgraph_size)
    for line in os.popen(cmd).readlines():
      feat, value = line.split()
      if feat not in feat_id:
        feat_id[feat] = current_feat
        current_feat += 1
      feat = feat_id[feat]
      features[feat] = float(value)
    data.append(features.copy())
    print 'Processed ', len(data)
  data = np.array(data)
  np.savetxt(output, data, delimiter=',')

if __name__ == '__main__':
  main()
