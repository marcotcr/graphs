#!/usr/bin/python
from __future__ import division
import argparse
import numpy as np
import scipy
import scipy.optimize
import os
import collections

def f(p,q,pi, i):
  if i == 0:
    return (1 - pi) ** 3 * (1 - p) **3 + 3 * pi * (1 - pi) ** 2 * (1 - p) * (1 - q) ** 2 + 3 * pi**2*(1 - pi) * (1 - p) * (1 - q) ** 2 + pi ** 3 * (1 - p)**3
  if i == 1:
    return (1 - pi) ** 3 * p * (1 - p) **2 + pi * (1 - pi) ** 2 * (2 * q * (1 - q) * (1 - p) + p * (1 - q) **2) + pi ** 2 * (1 - pi) * (2 * q * (1 - q) * (1 - p) + p* (1 - q) ** 2) + pi ** 3 * p * (1 - p) **2
  if i == 2:
    return (1 - pi) ** 3 * (1 - p) * (p) **2 + pi * (1 - pi) ** 2 * (2 * q * (1 - q) * (p) + (1 - p) * (q) **2) + pi ** 2 * (1 - pi) * (2 * q * (1 - q) * (p) + (1 - p)* (q) ** 2) + pi ** 3 * (1 - p) * (p) **2
  if i == 3:
    return (1 - pi) ** 3 * (p) **3 + 3 * pi * (1 - pi) ** 2 * (p) * (q) ** 2 + 3 * pi**2*(1 - pi) * (p) * (q) ** 2 + pi ** 3 * (p)**3
  else:
    return 1
    
    
def likelihood(params, *values):
  print 'p', params
  p, q, pi = params
  if p < 0 or q < 0 or pi < 0:
    return 10000000000000
  if p > 1 or q > 1 or pi > 1:
    return 10000000000000
  total = 0
  # TODO: check if count vector is giving us correct values
  for i, xi in enumerate(values):
    if np.isnan(np.log(max(0.0000000000001, f(p,q,pi,i)))):
      print f(p,q,pi,i)
      print 'oi'
      quit()
    total += xi * np.log(max(.0000000000001, f(p,q,pi, i)))
  print 'ret', -1 * total
  return -1 * total
    
    
def main():
  # parser = argparse.ArgumentParser(description='Generate a graph with block model')
  # parser.add_argument('-n', '--nodes', required=True, type=int, dest='n')
  # parser.add_argument('-p', required=True, type=float, dest='p')
  # parser.add_argument('-q', required=True, type=float, dest='q')
  # parser.add_argument('-i', '--pi', required=True, dest='pi', type=float)
  # args = parser.parse_args()
  counts = [0.1679,0.3342,0.3346,0.1633]
  counts = [0.4169,0.4592,0.0818,0.0421]
  # 10000, p=1, q=0, pi = .5
  counts = [0.4146, 0.4577, 0.0862, 0.0415]

  # likelihood([.1, .2, .3], counts)
  def c1(x):
    return x[0]
  def c2(x):
    return x[1]
  def c3(x):
    return x[2]
  def c4(x):
    return 1.00000000000000000000 - x[0]
  def c5(x):
    return 1.00000000000000000000 - x[1]
  def c6(x):
    return 1.00000000000000000000 - x[2]

  #print scipy.optimize.minimize(likelihood, (1, 0, .2), args=counts,
  #method='COBYLA',constraints=[c1,c2,c3,c4,c5,c6], bounds=[(0,1), (0,1), (0,1)])
  print scipy.optimize.fmin_cobyla(likelihood, (.5,.5,.5), args=counts,
  cons=[c1,c2,c3,c4,c5,c6], consargs=(), maxfun=100000)

         
    
  

if __name__ == '__main__':
  main()
