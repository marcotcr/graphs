import os
import sys
def GenerateML(p, q, s):
  data = '../ml_data/data_%s_%s_%s' % (p, q, s)
  labels = '../ml_data/fake_labels_%s_%s' % (p, q)
  cmd = 'python ml.py -d %s -l %s -f > ml_results/%s_%s_%s' % (data, labels, p, q, s)
  print cmd
  os.system(cmd)

#machine = sys.argv[1]
qs=[0.001,0.01,0.02,0.05,0.1,0.2,0.5]
sizes = [4,5,6, 'sink']
for q in qs:
  p = 2 * q
  for size in sizes:
    GenerateML(p,q, size)

q = 0.01
cs = [1,2,3,4,5]
for c in cs:
  p = c * q
  for size in sizes:
    GenerateML(p,q, size)
