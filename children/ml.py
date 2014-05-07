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
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.metrics import *
import sklearn.dummy

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
  # Normalizing data
  data = preprocessing.scale(data)
  preds_1 = np.zeros(data.shape[0])
  preds_2 = np.zeros(data.shape[0])
  preds_3 = np.zeros(data.shape[0])
  preds_4 = np.zeros(data.shape[0])
  for train_index, test_index in cross_validation.KFold(data.shape[0], n_folds=5):
    print 'Running for a split...'
    estimator = LogisticRegression()
    estimator.fit(data[train_index], labels[train_index])
    preds_1[test_index] = estimator.predict(data[test_index])

    estimator = sklearn.dummy.DummyClassifier(strategy='stratified',random_state=0)
    estimator.fit(data[train_index], labels[train_index])
    preds_2[test_index] = estimator.predict(data[test_index])

    estimator = RandomForestClassifier(n_estimators=20, n_jobs=5)
    estimator.fit(data[train_index], labels[train_index])
    preds_3[test_index] = estimator.predict(data[test_index])

    estimator = svm.LinearSVC()
    estimator.fit(data[train_index], labels[train_index])
    preds_4[test_index] = estimator.predict(data[test_index])

  print '-----------------'
  print 'LogReg'
  print classification_report(labels, preds_1)
  print 'Final f1 score:', f1_score(labels, preds_1)
  print '-----------------'
  print 'Baseline'
  print classification_report(labels, preds_2)
  print 'Final f1 score:', f1_score(labels, preds_2)
  print '-----------------'
  print 'RandomForest'
  print classification_report(labels, preds_3)
  print 'Final f1 score:', f1_score(labels, preds_3)
  print '-----------------'
  print 'SVM'
  print classification_report(labels, preds_4)
  print 'Final f1 score:', f1_score(labels, preds_4)

if __name__ == '__main__':
  main()
