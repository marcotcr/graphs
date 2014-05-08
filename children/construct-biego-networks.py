import argparse
import collections

def main():
  parser = argparse.ArgumentParser(description='Generate bi-ego networks. Writes files that are named node1-node2.edges')
  parser.add_argument('-o', required=True,  dest='output_folder', help='output folder')
  parser.add_argument('-e', required=True, dest='edges', help='edge file')
  parser.add_argument('-n', required=True, dest='nodes', help='node attribute file')
  args = parser.parse_args()
  node_gender = {}
  for line in open(args.nodes):
    node, gender = line.split()[0], line.strip().split()[2]
    if gender == 'M' or gender == 'F':
      node_gender[node] = gender
  neighbors = collections.defaultdict(lambda: set())
  for line in open(args.edges):
    node1, node2 = line.strip().split()
    neighbors[node1].add(node2)      
    neighbors[node2].add(node1)      
  statistics = open('corpus-statistics', 'w')
  for line in open(args.edges):
    node1, node2 = line.strip().split()
    if node1 in node_gender and node2 in node_gender:
      output = open('%s/%s-%s.edges' % (args.output_folder, node1, node2), 'w')
      all_nodes = neighbors[node1].union(neighbors[node2])
      all_nodes.remove(node1)
      all_nodes.remove(node2)
      edges = 0
      for node in all_nodes:
        for neb in neighbors[node]:
          if neb in all_nodes:
            output.write('%s %s\n' % (node, neb))
            edges += 1
      statistics.write('%s-%s %d %d %d %d %s\n' % (node1, node2, len(neighbors[node1]), len(neighbors[node2]), len(all_nodes), len(neighbors[node1].intersection(neighbors[node2])), edges))
      output.close()

if __name__ == '__main__':
  main()
