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
import sklearn
from sklearn import cross_validation
from sklearn import svm

def Usage():
  print '%s' % sys.argv[0]
  print 'Options:'
  print '-d (required): data file'
  print '-l (required): label file'
  print 'Example usage:'
  print 'python ml.py -d data -l labels' 
  quit()

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "d:l:")
  except getopt.GetoptError, err:
    print str(err)
    Usage()
  data_file = None
  label_file = None
  for option, value in opts:
    if option == "-h":
      Usage()
    elif option == '-d':
      data_file = value
    elif option == '-l':
      label_file = value
    else:
      assert False, "Option %s not available" % option
  if not data_file or not label_file:
    Usage()
  data = np.genfromtxt(data_file, delimiter=',')
  labels = np.genfromtxt(label_file, delimiter='\n')
  estimator = svm.SVC()
  print 'Acc',
  print np.mean(cross_validation.cross_val_score(estimator, data, labels, cv=cross_validation.LeaveOneOut(data.shape[0]), scoring='accuracy'))
  #print 'F1',
  #print np.mean(cross_validation.cross_val_score(estimator, data, labels, cv=cross_validation.LeaveOneOut(data.shape[0]), scoring='f1'))
  #print 'AUC',
  #print np.mean(cross_validation.cross_val_score(estimator, data, labels, cv=cross_validation.LeaveOneOut(data.shape[0]), scoring='roc_auc'))
  #for train_index, test_index in cross_validation.LeaveOneOut(data.shape[0]):
    #print train_index, test_index

if __name__ == '__main__':
  main()
