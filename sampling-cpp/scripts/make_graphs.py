import os
import sys
import matplotlib
import collections
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import *
def GenerateML(p, q, s):
  data = 'ml_results/%s_%s_%s' % (p, q, s)
  return [x.strip().split() for x in open(data).readlines()]

#machine = sys.argv[1]
qs=[0.001,0.01,0.02,0.05,0.1,0.2,0.5]
sizes = [4,5,6]#, 'sink']
metric_index = {'name':0, 'avg_prec': 1, 'avg_recall':2, 'avg_f1': 3, 'prec_1':
4, 'recall_1':5, 'f1_1':6, 'prec_0': 7, 'recall_0':8, 'f1_0': 9}
metric = 'avg_f1'

algorithm_results = collections.defaultdict(lambda: [])
algorithms = set()
for q in qs:
  p = 2 * q
  for size in sizes:
    for x in GenerateML(p,q, size):
      algorithm_results[x[metric_index['name']] + '_' + str(size)].append(x)
      algorithms.add(x[metric_index['name']])

for alg in algorithms:
  plt.figure()
  plt.xlabel('q')
  plt.ylabel(metric)
  plt.title('p = 2q, %s' % alg)
  for size in sizes:
    name = alg + '_' + str(size)
    plt.plot(qs, [x[metric_index[metric]] for x in algorithm_results[name]], label=name)
  plt.legend()
  plt.savefig('p2q_%s.png' % alg)

plt.figure()
plt.xlabel('q')
plt.ylabel(metric)
plt.title('p = 2q, size=%d' % max(sizes))
for alg in algorithms:
  name = alg + '_' + str(max(sizes))
  plt.plot(qs, [x[metric_index[metric]] for x in algorithm_results[name]], label=name)
plt.legend()
plt.savefig('p2q_all_size%d.png' % max(sizes))

algorithm_results = collections.defaultdict(lambda: [])
algorithms = set()
q = 0.01
cs = [1,2,3,4,5]
for c in cs:
  p = c * q
  for size in sizes:
    for x in GenerateML(p,q, size):
      algorithm_results[x[metric_index['name']] + '_' + str(size)].append(x)
      algorithms.add(x[metric_index['name']])


for alg in algorithms:
  plt.figure()
  plt.xlabel('c')
  plt.ylabel(metric)
  plt.title('p = cq, q=0.01, %s' % alg)
  for size in sizes:
    name = alg + '_' + str(size)
    plt.plot(cs, [x[metric_index[metric]] for x in algorithm_results[name]], label=name)
  plt.legend()
  plt.savefig('pcq_%s.png' % alg)

plt.figure()
plt.xlabel('q')
plt.ylabel(metric)
plt.title('p = cq, q=0.01 size=%d' % max(sizes))
for alg in algorithms:
  name = alg + '_' + str(max(sizes))
  plt.plot(cs, [x[metric_index[metric]] for x in algorithm_results[name]], label=name)
plt.legend()
plt.savefig('pcq_all_size%d.png' % max(sizes))

