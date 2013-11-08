#!/usr/bin/python
import sys
import getopt
import collections
import os
import re
import numpy as np
from numpy import *
from sklearn import linear_model
from sklearn import cross_validation

def Usage():
  print '%s' % sys.argv[0]
  print 'Options:'
  print '-i (required): training file'
  print '-l (required): label file'
  print 'Example usage:'
  print '%s -i 3-vector-counts -l entropy' % sys.argv[0]
  quit()

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "i:l:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  train_file = None
  label_file = None
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-i':
      train_file = value
    elif option == '-l':
      label_file = value
    else:
      assert False, "Option %s not available" % option
  if not train_file or not label_file:
    Usage()
  map_to_line = {}
  current_line = 0
  entropies = []
  for line in open(label_file):
    target_node, entropy = line.strip().split(',')
    if target_node not in map_to_line:
      map_to_line[target_node] = current_line
      current_line += 1
    entropies.append(float(entropy))
  
  Y = np.array(entropies)
  a = open(train_file , 'r')
  dimensionality = len(a.readline().split(',')) - 1
  a.close()
  X = zeros((len(Y), dimensionality))
  for line in open(train_file):
    temp = line.strip().split(',')
    target_node = temp[0]
    line_id = map_to_line[target_node]
    X[line_id] = array(map(float, temp[1:]))
  loo = cross_validation.LeaveOneOut(n=X.shape[0])
  lr_output = open('%slinear_regression.output' % train_file, 'w')
  ridge_output = open('%sridge.output' % train_file, 'w')

  for train, test in loo:
    lr    = linear_model.LinearRegression()
    ridge = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
    lr.fit(X[train], Y[train])
    ridge.fit(X[train], Y[train])
    # This is a workaround the fact that entropy has to be > 0
    lr_output.write('%s %s\n' % (Y[test][0], max(0, lr.predict(X[test][0]))))
    ridge_output.write('%s %s\n' % (Y[test][0], max(0, ridge.predict(X[test][0]))))

    


if __name__ == '__main__':
  main()
