#!/usr/bin/python
from __future__ import division
import argparse
import numpy as np
import scipy
import os
import collections

def main():
  parser = argparse.ArgumentParser(description='Generate a graph with block model')
  parser.add_argument('-n', '--nodes', required=True, type=int, dest='n')
  parser.add_argument('-p', required=True, type=float, dest='p')
  parser.add_argument('-q', required=True, type=float, dest='q')
  parser.add_argument('-i', '--pi', required=True, dest='pi', type=float)
  args = parser.parse_args()
  assignment = np.random.binomial(1, args.pi, args.n)
  graph = collections.defaultdict(lambda: collections.defaultdict(lambda: False))
  for i in range(args.n):
    for j in range(i + 1, args.n):
      if assignment[i] == assignment[j]:
        p = args.p
      else:
        p = args.q
      edge = np.random.binomial(1, p)
      if edge:
        graph[i][j] = True
        graph[j][i] = True
  for x in graph:
    for y in graph[x]:
      if x < y:
        print x,y
         
    
  

if __name__ == '__main__':
  main()
