import os
qs=[0.001,0.01,0.02,0.05,0.1,0.2,0.5]
def GenerateGraph(p, q):
  cmd = 'python generate_graphs.py -n 2000 -p %s -q %s -i 0.5 > sampling-cpp/raw_data/fake_edges_%s_%s' % (p, q, p, q)
  print cmd
  os.system(cmd)
  cmd = 'mv nodes sampling-cpp/raw_data/fake_nodes_%s_%s' % (p, q)
  print cmd
  os.system(cmd)

for q in qs:
  p = 2 * q
  GenerateGraph(p,q)
q = 0.01
for c in [1,2,3,4,5]:
  p = c * q
  GenerateGraph(p, q)
