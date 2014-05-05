from __future__ import division
import itertools
import collections
import sys
import os
class all_graphs(object):
  def __init__(self, n, complement=False):
    self.n = n
    self.edges = int(n * (n - 1) / 2)
    self.generator = itertools.product([0,1], repeat=self.edges)
    self.complement = complement
  def __iter__(self):
    return self
  def __next__(self):
    return self.next()
  def next(self):
    try:
      active = self.generator.next()
    except:
      raise StopIteration
    edge_count = 0
    graph = collections.defaultdict(lambda: collections.defaultdict(lambda: False))
    for i in range(self.n):
      graph[i]
      for j in range(i + 1, self.n):
        if not self.complement:
          if active[edge_count]:
            graph[i][j] = True
            graph[j][i] = True
          edge_count += 1
        else:
          if not active[edge_count]:
            graph[i][j] = True
            graph[j][i] = True
          edge_count += 1
    return graph

def GetCanonical(graph):
  WriteToNauty(graph)
  cmd = '/Users/marcotcr/Downloads/nauty25r9/dreadnaut < /tmp/nauty | grep :'
  can = os.popen(cmd).read()
  return can

def WriteToNauty(graph):
  nodes = sorted(graph.keys())
  nauty = open('/tmp/nauty', 'w')
  nauty.write('n=%d g\n' % len(nodes))
  for node in nodes:
    nauty.write('%d : %s\n' % (node, ' '.join(map(str, sorted(graph[node].keys()))) + ';'))
  nauty.write('-a-mcx\n')
  nauty.write('b\n')
  nauty.close()
def NumberOfEdges(graph):
  edges = 0
  for x in graph:
    edges += len(graph[x])
  return 'Edges:%d'  % (edges / 2)

def DegreeDistribution(graph):
  # This only works for graphs up to size 10
  out = ''
  for x in graph:
    out += '%d' % len(graph[x])
  return 'DegreeDistribution:'+''.join(sorted(out))

def ConnectedComponents(graph):
  """Sizes of connected components"""
  nodes = set(graph.keys())
  ccs = 0
  size_ccs = []
  while nodes:
    size_cc = 0
    Q = [nodes.pop()]
    while Q:
      x = Q.pop(0)
      size_cc += 1
      for y in graph[x]:
        if y in nodes:
          nodes.remove(y)
          Q.append(y)
    size_ccs.append(size_cc)  
  return 'CCS:'+ ''.join(map(str,sorted(size_ccs)))

def Bipartite(graph):
  """Sizes of connected components"""
  nodes = set(graph.keys())
  colors = collections.defaultdict(lambda: 'R')
  while nodes:
    Q = [nodes.pop()]
    colors[Q[0]] = 'R'
    while Q:
      x = Q.pop(0)
      for y in graph[x]:
        if y in colors:
          if colors[y] == colors[x]:
            return 'Bipartite:F'
        else:
          colors[y] = 'B' if colors[x] == 'R' else 'R'
        if y in nodes:
          nodes.remove(y)
          Q.append(y)
  return 'Bipartite:T'

def LongestShortestPath(graph, node):
  Q = [node]
  distances = {x:9 for x in graph.keys()}
  distances[node] = 0
  visited = set([node])
  while Q:
    x = Q.pop(0)
    for y in graph[x]:
      if y not in visited:
        distances[y] = distances[x] + 1
        Q.append(y)
        visited.add(y)
  return max(distances.values())

def MST(graph):
  nodes = set(graph.keys())
  edges = 0
  while nodes:
    Q = [nodes.pop()]
    while Q:
      x = Q.pop(0)
      for y in graph[x]:
        if y in nodes:
          nodes.remove(y)
          edges += 1
          Q.append(y)
  return 'MST:' + str(edges)
        
def NodesAtDistanceK(graph, node, k):
  Q = [node]
  distances = {x:9 for x in graph.keys()}
  distances[node] = 0
  visited = set([node])
  while Q:
    x = Q.pop(0)
    for y in graph[x]:
      if y not in visited:
        distances[y] = distances[x] + 1
        Q.append(y)
        visited.add(y)
  return len([x for x in distances.values() if x ==k])


    
def LongestShortestPathDistribution(graph):
  nodes = set(graph.keys())
  return 'LSP:'+ ''.join(map(str,sorted([LongestShortestPath(graph, node) for node in nodes])))

def NodesAtDistanceKDistribution(graph, k):
  nodes = set(graph.keys())
  return 'ND%d:' % k + ''.join(map(str,sorted([NodesAtDistanceK(graph, node, k) for node in nodes])))

def Diameter(graph):
  nodes = set(graph.keys())
  return 'diameter:%d' % max([LongestShortestPath(graph, node) for node in nodes])

  

def FeatureSwitch(graph, feature):
  if feature == 'number_of_edges':
    return NumberOfEdges(graph)
  if feature == 'degree_distribution':
    return DegreeDistribution(graph)
  if feature == 'ccs':
    return ConnectedComponents(graph)
  if feature == 'longest_shortest_path':
    return LongestShortestPathDistribution(graph)
  if feature == 'diameter':
    return Diameter(graph)
  if feature == 'bipartite':
    return Bipartite(graph)
  if feature == 'mst':
    return MST(graph)
  if feature == 'nodes_at':
    return_ = ''
    for i in range(10):
      return_ += NodesAtDistanceKDistribution(graph, i) + '-'
    return return_

n = int(sys.argv[1])
graphs = all_graphs(n)
complements = all_graphs(n, complement=True)
features = ['number_of_edges', 'degree_distribution', 'ccs',
'longest_shortest_path', 'nodes_at', 'mst', 'bipartite']
features = ['degree_distribution', 'ccs', 'bipartite', 'longest_shortest_path']
#features = ['degree_distribution', 'ccs', 'longest_shortest_path']

u_graphs = set()
count = 0
keep_graphs = []
for graph, complement in itertools.izip(graphs, complements):
  if count % 100 == 0:
    print count
  #rep = GetCanonical(graph)
  rep = ''
  for feature in features:
    rep += '%s-' % FeatureSwitch(graph, feature)
  for feature in features:
    rep += 'Complement%s-' % FeatureSwitch(complement, feature)
  rep = rep.strip('-')
  # print graph, rep
  # print rep
  u_graphs.add(rep)
  count += 1
    
print 'Number of graphs of size %d = %d' % (n, count)
print 'Unique graphs of size %d    = %d' % (n, len(u_graphs))
# print sorted(u_graphs)
    
