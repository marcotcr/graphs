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
  print '-l (required): output label file'
  print '-o (required): output data file'
  print 'Example usage:'
  print 'python construct_feature_vectors.py -d ../../gplus/ -n 1 -s 5 -l labels -o data' 
  quit()

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "d:s:n:l:o:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  dataset_folder = None
  n_samples = None
  subgraph_size = None
  labels = None
  output = None
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-d':
      dataset_folder = value
    elif option == '-n':
      n_samples = int(value)
    elif option == '-s':
      subgraph_size = int(value)
    elif option == '-l':
      labels = open(value, 'w')
    elif option == '-o':
      output = value 
    else:
      assert False, "Option %s not available" % option
  if not dataset_folder or not n_samples or not subgraph_size or not labels or not output:
    Usage()
  
  possible_subgraphs = {3: 4, 4: 11, 5: 34, 6: 156, 7: 1044, 8: 12346, 9: 274668, 10: 12005168}
  k = possible_subgraphs[subgraph_size]
  current_feat = 0
  feat_id = {}
  data = []
  graphs = [re.sub('.edges', '', re.sub('%s/' % dataset_folder, '', x.strip())) for x in os.popen('ls %s/*.edges' % dataset_folder).readlines()]
  print 'Total:', len(graphs)
  for graph in graphs:
    edge_file = '%s/%s.edges' % (dataset_folder, graph)
    feature_file = '%s/%s.egofeat' % (dataset_folder, graph)
    try:
      gender = open(feature_file, 'r').read().split()[:3].index('1')
    except:
      continue
    labels.write('%s\n' % gender)
    features = np.zeros(k) 
    cmd = 'python sample_subgraphs.py -e %s -n %d -s %d' % (edge_file, n_samples, subgraph_size)
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
