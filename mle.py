#!/usr/bin/python
from __future__ import division
import argparse
import numpy as np
import scipy
import scipy.optimize
import os
import collections

DEBUG = False

def prob_x_blacks(number_of_blacks, pi):
  """Assuming nodes are either black or white, and that there are three nodes.
  Returns the probability of observing a specific number of black nodes."""
  if number_of_blacks == 0:
    return (1 - pi) ** 3
  if number_of_blacks == 1:
    return pi * (1 - pi) ** 2
  if number_of_blacks == 2:
    return pi ** 2 * (1 - pi)
  if number_of_blacks == 3:
    return pi ** 3
  else:
    return 0
    

def f(p,q,pi, i):
  if i == 0:
    #return (1 - pi) ** 3 * (1 - p) **3 + 3 * pi * (1 - pi) ** 2 * (1 - p) * (1 - q) ** 2 + 3 * pi**2*(1 - pi) * (1 - p) * (1 - q) ** 2 + pi ** 3 * (1 - p)**3
    all_white = prob_x_blacks(0, pi) * (1 - p) ** 3
    one_black = prob_x_blacks(1, pi) * 3 * (1 - p) * (1 - q) ** 2
    two_blacks = prob_x_blacks(2, pi) * 3 * (1 - p) * (1 - q) ** 2
    all_black = prob_x_blacks(3, pi) * (1 - p) ** 3
    return all_black + one_black + two_blacks + all_white
  if i == 1:
    #return (1 - pi) ** 3 * p * (1 - p) **2 + pi * (1 - pi) ** 2 * (2 * q * (1 - q) * (1 - p) + p * (1 - q) **2) + pi ** 2 * (1 - pi) * (2 * q * (1 - q) * (1 - p) + p* (1 - q) ** 2) + pi ** 3 * p * (1 - p) **2
    all_white = prob_x_blacks(0, pi) * 3 * p * (1 - p) ** 2
    one_black = prob_x_blacks(1, pi) * (6 * q * (1 - q) * (1 - p) + 3 * p * (1 - q) **2)
    two_blacks = prob_x_blacks(2, pi) * (6 * q * (1 - q) * (1 - p) + 3 * p * (1 - q) **2)
    all_black = prob_x_blacks(3, pi) * 3 * p * (1 - p) ** 2
    return all_black + one_black + two_blacks + all_white
  if i == 2:
    #return (1 - pi) ** 3 * (1 - p) * (p) **2 + pi * (1 - pi) ** 2 * (2 * q * (1 - q) * (p) + (1 - p) * (q) **2) + pi ** 2 * (1 - pi) * (2 * q * (1 - q) * (p) + (1 - p)* (q) ** 2) + pi ** 3 * (1 - p) * (p) **2
    all_white = prob_x_blacks(0, pi) * 3 * p**2 * (1 -p)
    one_black = prob_x_blacks(1, pi) * (6 * q * (1 - q) * p + 3 * (1 - p) * q **2)
    two_blacks = prob_x_blacks(2, pi) * (6 * q * (1 - q) * p + 3 * (1 - p) * q **2)
    all_black = prob_x_blacks(3, pi) * 3 * p**2 * (1 -p)
    return all_black + one_black + two_blacks + all_white
  if i == 3:
    #return (1 - pi) ** 3 * (p) **3 + 3 * pi * (1 - pi) ** 2 * (p) * (q) ** 2 + 3 * pi**2*(1 - pi) * (p) * (q) ** 2 + pi ** 3 * (p)**3
    all_white = prob_x_blacks(0, pi) * p ** 3
    one_black = prob_x_blacks(1, pi) * 3 * q ** 2 * p
    two_blacks = prob_x_blacks(2, pi) * 3 * q ** 2 * p
    all_black = prob_x_blacks(3, pi) * p ** 3
    return all_black + one_black + two_blacks + all_white
  else:
    return 0
    
    
def likelihood(params, *values):
  p, q, pi = params
  if DEBUG:
    print 'p: %.2f q: %.2f pi:%.2f' % (p, q, pi)
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
    if DEBUG:
      print xi, f(p,q,pi,i)

    total += (xi - f(p,q,pi,i)) ** 2

    # total += xi * np.log(max(.0000000000001, f(p,q,pi, i)))
  # print 'ret', -1 * total
  # return -1 * total
  # print 'ret', total
  return total
    
    
class Instance:
  def __init__(self, counts, true_p, true_q, true_pi, N):
    self.true_p = true_p
    self.true_q = true_q
    self.true_pi = true_pi
    self.counts = counts
    self.N = N
def main():
  # parser = argparse.ArgumentParser(description='Generate a graph with block model')
  # parser.add_argument('-n', '--nodes', required=True, type=int, dest='n')
  # parser.add_argument('-p', required=True, type=float, dest='p')
  # parser.add_argument('-q', required=True, type=float, dest='q')
  # parser.add_argument('-i', '--pi', required=True, dest='pi', type=float)
  # args = parser.parse_args()

  instances = []
  counts = [0.00000001,0.732,0.000001,0.268]
  instances.append(Instance(counts, 1, 0, .5, 10000))

  counts = [ 0.0000001,0.7499,0.00000001,0.2501]
  instances.append(Instance(counts, 1, 0, .5, 1000))

  counts = [ 0.0629,0.331, 0.3185,0.2876]
  instances.append(Instance(counts, .8, .2, .2, 10000))
  counts = [ 0.0692, 0.3403, 0.3137, 0.2768]
  instances.append(Instance(counts, .8, .2, .2, 1000))

  counts = [ 0.0629, 0.5632, 0.0991, 0.2748] 
  instances.append(Instance(counts, .9, .01, .3, 10000))
  counts =[ 0.0627,0.5708,0.0962,0.2703] 
  instances.append(Instance(counts, .9, .01, .3, 1000))
  
  ############## new
  instances = []
  counts = [0.7574,0.2084,0.0342,0.00000000001]
  instances.append(Instance(counts, 0, 0.25, 0.25, 1000))
  counts = [0.6791,0.2761,0.0448,0.00000000001]
  instances.append(Instance(counts, 0, 0.25, 0.5, 1000))
  counts = [0.7376,0.2244,0.038,0.00000000001]
  instances.append(Instance(counts, 0, 0.25, 0.75, 1000))
  counts = [0.549,0.3022,0.1488,0.00000000001]
  instances.append(Instance(counts, 0, 0.5, 0.25, 1000))
  counts = [0.4457,0.3684,0.1859,0.00000000001]
  instances.append(Instance(counts, 0, 0.5, 0.5, 1000))
  counts = [0.589,0.2792,0.1318,0.00000000001]
  instances.append(Instance(counts, 0, 0.5, 0.75, 1000))
  counts = [0.4683,0.2185,0.3132,0.00000000001]
  instances.append(Instance(counts, 0, 0.75, 0.25, 1000))
  counts = [0.2995,0.2831,0.4174,0.00000000001]
  instances.append(Instance(counts, 0, 0.75, 0.5, 1000))
  counts = [0.4946,0.2047,0.3007,0.00000000001]
  instances.append(Instance(counts, 0, 0.75, 0.75, 1000))
  counts = [0.4512,0.00000000001,0.5488,0.00000000001]
  instances.append(Instance(counts, 0, 1, 0.25, 1000))
  counts = [0.2438,0.00000000001,0.7562,0.00000000001]
  instances.append(Instance(counts, 0, 1, 0.5, 1000))
  counts = [0.4567,0.00000000001,0.5433,0.00000000001]
  instances.append(Instance(counts, 0, 1, 0.75, 1000))
  counts = [0.4273,0.4179,0.1388,0.016]
  instances.append(Instance(counts, 0.25, 0, 0, 1000))
  counts = [0.5964,0.3316,0.066,0.006]
  instances.append(Instance(counts, 0.25, 0, 0.25, 1000))
  counts = [0.6674,0.2938,0.0347,0.0041]
  instances.append(Instance(counts, 0.25, 0, 0.5, 1000))
  counts = [0.5944,0.3322,0.0668,0.0066]
  instances.append(Instance(counts, 0.25, 0, 0.75, 1000))
  counts = [0.426,0.4242,0.134,0.0158]
  instances.append(Instance(counts, 0.25, 0.25, 0, 1000))
  counts = [0.4262,0.4214,0.1353,0.0171]
  instances.append(Instance(counts, 0.25, 0.25, 0.25, 1000))
  counts = [0.4183,0.4242,0.1406,0.0169]
  instances.append(Instance(counts, 0.25, 0.25, 0.5, 1000))
  counts = [0.4198,0.4237,0.1409,0.0156]
  instances.append(Instance(counts, 0.25, 0.25, 0.75, 1000))
  counts = [0.4282,0.4165,0.1412,0.0141]
  instances.append(Instance(counts, 0.25, 0.25, 1, 1000))
  counts = [0.4196,0.4237,0.1394,0.0173]
  instances.append(Instance(counts, 0.25, 0.5, 0, 1000))
  counts = [0.2864,0.4304,0.2402,0.043]
  instances.append(Instance(counts, 0.25, 0.5, 0.25, 1000))
  counts = [0.2427,0.4379,0.2732,0.0462]
  instances.append(Instance(counts, 0.25, 0.5, 0.5, 1000))
  counts = [0.2816,0.4248,0.2471,0.0465]
  instances.append(Instance(counts, 0.25, 0.5, 0.75, 1000))
  counts = [0.4122,0.4276,0.1435,0.0167]
  instances.append(Instance(counts, 0.25, 0.5, 1, 1000))
  counts = [0.4206,0.4212,0.1411,0.0171]
  instances.append(Instance(counts, 0.25, 0.75, 0, 1000))
  counts = [0.2064,0.357,0.3472,0.0894]
  instances.append(Instance(counts, 0.25, 0.75, 0.25, 1000))
  counts = [0.1442,0.3242,0.4222,0.1094]
  instances.append(Instance(counts, 0.25, 0.75, 0.5, 1000))
  counts = [0.223,0.3485,0.3476,0.0809]
  instances.append(Instance(counts, 0.25, 0.75, 0.75, 1000))
  counts = [0.4206,0.42,0.1422,0.0172]
  instances.append(Instance(counts, 0.25, 0.75, 1, 1000))
  counts = [0.4147,0.4248,0.143,0.0175]
  instances.append(Instance(counts, 0.25, 1, 0, 1000))
  counts = [0.1712,0.1726,0.4949,0.1613]
  instances.append(Instance(counts, 0.25, 1, 0.25, 1000))
  counts = [0.1007,0.1053,0.5978,0.1962]
  instances.append(Instance(counts, 0.25, 1, 0.5, 1000))
  counts = [0.2037,0.2002,0.4579,0.1382]
  instances.append(Instance(counts, 0.25, 1, 0.75, 1000))
  counts = [0.4164,0.4253,0.1405,0.0178]
  instances.append(Instance(counts, 0.25, 1, 1, 1000))
  counts = [0.1303,0.3709,0.3745,0.1243]
  instances.append(Instance(counts, 0.5, 0, 0, 1000))
  counts = [0.3326,0.4538,0.1604,0.0532]
  instances.append(Instance(counts, 0.5, 0, 0.25, 1000))
  counts = [0.4013,0.4726,0.0943,0.0318]
  instances.append(Instance(counts, 0.5, 0, 0.5, 1000))
  counts = [0.3368,0.4423,0.1672,0.0537]
  instances.append(Instance(counts, 0.5, 0, 0.75, 1000))
  counts = [0.1269,0.3772,0.3725,0.1234]
  instances.append(Instance(counts, 0.5, 0.25, 0, 1000))
  counts = [0.2124,0.4204,0.2947,0.0725]
  instances.append(Instance(counts, 0.5, 0.25, 0.25, 1000))
  counts = [0.2451,0.444,0.2585,0.0524]
  instances.append(Instance(counts, 0.5, 0.25, 0.5, 1000))
  counts = [0.2164,0.4329,0.2811,0.0696]
  instances.append(Instance(counts, 0.5, 0.25, 0.75, 1000))
  counts = [0.122,0.3783,0.3719,0.1278]
  instances.append(Instance(counts, 0.5, 0.25, 1, 1000))
  counts = [0.1204,0.3804,0.3695,0.1297]
  instances.append(Instance(counts, 0.5, 0.5, 0, 1000))
  counts = [0.1233,0.3785,0.3717,0.1265]
  instances.append(Instance(counts, 0.5, 0.5, 0.25, 1000))
  counts = [0.1241,0.3708,0.3799,0.1252]
  instances.append(Instance(counts, 0.5, 0.5, 0.5, 1000))
  counts = [0.1264,0.3775,0.3706,0.1255]
  instances.append(Instance(counts, 0.5, 0.5, 0.75, 1000))
  counts = [0.1267,0.3796,0.3715,0.1222]
  instances.append(Instance(counts, 0.5, 0.5, 1, 1000))
  counts = [0.1262,0.379,0.3755,0.1193]
  instances.append(Instance(counts, 0.5, 0.75, 0, 1000))
  counts = [0.0717,0.2865,0.4267,0.2151]
  instances.append(Instance(counts, 0.5, 0.75, 0.25, 1000))
  counts = [0.0553,0.2639,0.4428,0.238]
  instances.append(Instance(counts, 0.5, 0.75, 0.5, 1000))
  counts = [0.0753,0.2799,0.4352,0.2096]
  instances.append(Instance(counts, 0.5, 0.75, 0.75, 1000))
  counts = [0.1269,0.3707,0.3754,0.127]
  instances.append(Instance(counts, 0.5, 0.75, 1, 1000))
  counts = [0.1273,0.3777,0.3692,0.1258]
  instances.append(Instance(counts, 0.5, 1, 0, 1000))
  counts = [0.0531,0.1675,0.4566,0.3228]
  instances.append(Instance(counts, 0.5, 1, 0.25, 1000))
  counts = [0.0298,0.098,0.468,0.4042]
  instances.append(Instance(counts, 0.5, 1, 0.5, 1000))
  counts = [0.0574,0.1767,0.4356,0.3303]
  instances.append(Instance(counts, 0.5, 1, 0.75, 1000))
  counts = [0.1214,0.3807,0.3713,0.1266]
  instances.append(Instance(counts, 0.5, 1, 1, 1000))
  counts = [0.0173,0.1409,0.4188,0.423]
  instances.append(Instance(counts, 0.75, 0, 0, 1000))
  counts = [0.1522,0.4752,0.1838,0.1888]
  instances.append(Instance(counts, 0.75, 0, 0.25, 1000))
  counts = [0.1905,0.5953,0.11,0.1042]
  instances.append(Instance(counts, 0.75, 0, 0.5, 1000))
  counts = [0.1397,0.4785,0.1879,0.1939]
  instances.append(Instance(counts, 0.75, 0, 0.75, 1000))
  counts = [0.0155,0.1415,0.4149,0.4281]
  instances.append(Instance(counts, 0.75, 0.25, 0, 1000))
  counts = [0.082,0.3473,0.3533,0.2174]
  instances.append(Instance(counts, 0.75, 0.25, 0.25, 1000))
  counts = [0.1079,0.4125,0.3373,0.1423]
  instances.append(Instance(counts, 0.75, 0.25, 0.5, 1000))
  counts = [0.0855,0.3409,0.3571,0.2165]
  instances.append(Instance(counts, 0.75, 0.25, 0.75, 1000))
  counts = [0.0152,0.1451,0.4188,0.4209]
  instances.append(Instance(counts, 0.75, 0.25, 1, 1000))
  counts = [0.0177,0.1448,0.4207,0.4168]
  instances.append(Instance(counts, 0.75, 0.5, 0, 1000))
  counts = [0.0421,0.2303,0.4343,0.2933]
  instances.append(Instance(counts, 0.75, 0.5, 0.25, 1000))
  counts = [0.0498,0.2663,0.4331,0.2508]
  instances.append(Instance(counts, 0.75, 0.5, 0.5, 1000))
  counts = [0.0435,0.2304,0.4275,0.2986]
  instances.append(Instance(counts, 0.75, 0.5, 0.75, 1000))
  counts = [0.0182,0.145,0.4286,0.4082]
  instances.append(Instance(counts, 0.75, 0.5, 1, 1000))
  counts = [0.0158,0.1454,0.4219,0.4169]
  instances.append(Instance(counts, 0.75, 0.75, 0, 1000))
  counts = [0.0164,0.14,0.424,0.4196]
  instances.append(Instance(counts, 0.75, 0.75, 0.25, 1000))
  counts = [0.0168,0.141,0.4198,0.4224]
  instances.append(Instance(counts, 0.75, 0.75, 0.5, 1000))
  counts = [0.0155,0.1389,0.4206,0.425]
  instances.append(Instance(counts, 0.75, 0.75, 0.75, 1000))
  counts = [0.0152,0.1392,0.4278,0.4178]
  instances.append(Instance(counts, 0.75, 0.75, 1, 1000))
  counts = [0.0175,0.1399,0.4191,0.4235]
  instances.append(Instance(counts, 0.75, 1, 0, 1000))
  counts = [0.0089,0.0632,0.325,0.6029]
  instances.append(Instance(counts, 0.75, 1, 0.25, 1000))
  counts = [0.004,0.0363,0.297,0.6627]
  instances.append(Instance(counts, 0.75, 1, 0.5, 1000))
  counts = [0.0065,0.0552,0.3274,0.6109]
  instances.append(Instance(counts, 0.75, 1, 0.75, 1000))
  counts = [0.0151,0.1407,0.4298,0.4144]
  instances.append(Instance(counts, 0.75, 1, 1, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0, 0, 1000))
  counts = [0.00000000001,0.5646,0.00000000001,0.4354]
  instances.append(Instance(counts, 1, 0, 0.25, 1000))
  counts = [0.00000000001,0.7475,0.00000000001,0.2525]
  instances.append(Instance(counts, 1, 0, 0.5, 1000))
  counts = [0.00000000001,0.5533,0.00000000001,0.4467]
  instances.append(Instance(counts, 1, 0, 0.75, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0.25, 0, 1000))
  counts = [0.00000000001,0.2985,0.2007,0.5008]
  instances.append(Instance(counts, 1, 0.25, 0.25, 1000))
  counts = [0.00000000001,0.417,0.2818,0.3012]
  instances.append(Instance(counts, 1, 0.25, 0.5, 1000))
  counts = [0.00000000001,0.2986,0.2057,0.4957]
  instances.append(Instance(counts, 1, 0.25, 0.75, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0.25, 1, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0.5, 0, 1000))
  counts = [0.00000000001,0.1438,0.2929,0.5633]
  instances.append(Instance(counts, 1, 0.5, 0.25, 1000))
  counts = [0.00000000001,0.1922,0.3726,0.4352]
  instances.append(Instance(counts, 1, 0.5, 0.5, 1000))
  counts = [0.00000000001,0.1474,0.2829,0.5697]
  instances.append(Instance(counts, 1, 0.5, 0.75, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0.5, 1, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0.75, 0, 1000))
  counts = [0.00000000001,0.0341,0.2046,0.7613]
  instances.append(Instance(counts, 1, 0.75, 0.25, 1000))
  counts = [0.00000000001,0.0451,0.2909,0.664]
  instances.append(Instance(counts, 1, 0.75, 0.5, 1000))
  counts = [0.00000000001,0.0389,0.2059,0.7552]
  instances.append(Instance(counts, 1, 0.75, 0.75, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 0.75, 1, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 1, 0, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 1, 0.25, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 1, 0.5, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 1, 0.75, 1000))
  counts = [0.00000000001,0.00000000001,0.00000000001,1.]
  instances.append(Instance(counts, 1, 1, 1, 1000))
  counts = [0.7627,0.2029,0.0344,0.00000000001]
  instances.append(Instance(counts, 0, 0.25, 0.25, 10000))
  counts = [0.6743,0.2787,0.047,0.00000000001]
  instances.append(Instance(counts, 0, 0.25, 0.5, 10000))
  counts = [0.7575,0.2064,0.0361,0.00000000001]
  instances.append(Instance(counts, 0, 0.25, 0.75, 10000))
  counts = [0.5814,0.2818,0.1368,0.00000000001]
  instances.append(Instance(counts, 0, 0.5, 0.25, 10000))
  counts = [0.439,0.3729,0.1881,0.00000000001]
  instances.append(Instance(counts, 0, 0.5, 0.5, 10000))
  counts = [0.5796,0.2836,0.1368,0.00000000001]
  instances.append(Instance(counts, 0, 0.5, 0.75, 10000))
  counts = [0.4632,0.2141,0.3227,0.00000000001]
  instances.append(Instance(counts, 0, 0.75, 0.25, 10000))
  counts = [0.2982,0.2778,0.424,0.00000000001]
  instances.append(Instance(counts, 0, 0.75, 0.5, 10000))
  counts = [0.49,0.2072,0.3028,0.00000000001]
  instances.append(Instance(counts, 0, 0.75, 0.75, 10000))
  counts = [0.4397,0.00000000001,0.5603,0.00000000001]
  instances.append(Instance(counts, 0, 1, 0.25, 10000))
  counts = [0.2521,0.00000000001,0.7479,0.00000000001]
  instances.append(Instance(counts, 0, 1, 0.5, 10000))
  counts = [0.4467,0.00000000001,0.5533,0.00000000001]
  instances.append(Instance(counts, 0, 1, 0.75, 10000))
  counts = [0.4248,0.4214,0.1382,0.0156]
  instances.append(Instance(counts, 0.25, 0, 0, 10000))
  counts = [0.611,0.3237,0.0594,0.0059]
  instances.append(Instance(counts, 0.25, 0, 0.25, 10000))
  counts = [0.6657,0.2959,0.0351,0.0033]
  instances.append(Instance(counts, 0.25, 0, 0.5, 10000))
  counts = [0.605,0.3277,0.0591,0.0082]
  instances.append(Instance(counts, 0.25, 0, 0.75, 10000))
  counts = [0.4299,0.4189,0.1377,0.0135]
  instances.append(Instance(counts, 0.25, 0.25, 0, 10000))
  counts = [0.4277,0.412,0.1438,0.0165]
  instances.append(Instance(counts, 0.25, 0.25, 0.25, 10000))
  counts = [0.4264,0.419,0.1401,0.0145]
  instances.append(Instance(counts, 0.25, 0.25, 0.5, 10000))
  counts = [0.4243,0.4188,0.1405,0.0164]
  instances.append(Instance(counts, 0.25, 0.25, 0.75, 10000))
  counts = [0.4194,0.423,0.1434,0.0142]
  instances.append(Instance(counts, 0.25, 0.25, 1, 10000))
  counts = [0.4174,0.4238,0.1424,0.0164]
  instances.append(Instance(counts, 0.25, 0.5, 0, 10000))
  counts = [0.2898,0.4301,0.2334,0.0467]
  instances.append(Instance(counts, 0.25, 0.5, 0.25, 10000))
  counts = [0.2486,0.4288,0.2683,0.0543]
  instances.append(Instance(counts, 0.25, 0.5, 0.5, 10000))



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

  for instance in instances:
  # Other methods: 'SLSQP', TNC, L-BFGS-B
    if instance.true_pi > 0.5:
      continue
    best = ((0,0,0), 10000)
    # Here I am initializing the parameters 10 times, and picking the best
    # result.
    for i in range(10):
      pi = np.random.uniform(0, .5)
      p = np.random.random()
      q = np.random.random()
      a = scipy.optimize.minimize(likelihood, (p, q, pi), args=instance.counts,
      method='SLSQP', bounds=[(0,1), (0,1), (0,.5)])
      p, q, pi = a.x
      l = likelihood((p,q,pi), *instance.counts)
      if l < best[1]:
        best = (a, l)
    a = best[0]
    if DEBUG:
      print a
      print
    print
    print 'Nsamples:', instance.N
    print 'True:'
    p, q, pi = instance.true_p, instance.true_q, instance.true_pi
    print 'p: %.2f q: %.2f pi:%.2f' % (p, q, pi)
    p, q, pi = a.x
    print 'Likelihood', likelihood((p,q,pi), *instance.counts)
    print 'Predicted:'
    print 'p: %.2f q: %.2f pi:%.2f' % (p, q, pi)
    print 'TCounts:', ['%.3f ' % z for z in instance.counts]
    print 'Ecounts:', ['%.3f' % z for z in [f(p,q,pi, x) for x in range(4)]]
    p, q, pi = instance.true_p, instance.true_q, instance.true_pi
    print 'Zcounts:', ['%.3f' % z for z in [f(p,q,pi, x) for x in range(4)]]
    #print scipy.optimize.fmin_cobyla(likelihood, (.5,.5,.5), args=counts,
    #cons=[c1,c2,c3,c4,c5,c6], consargs=(), maxfun=100000)

         
    
  

if __name__ == '__main__':
  main()
