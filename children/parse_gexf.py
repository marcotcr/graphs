from xml.dom import minidom
import argparse

def main():
  parser = argparse.ArgumentParser(description='Generate a graph and a node attribute file from gexf file')
  parser.add_argument('-i', required=True,  dest='input', help='Input gexf file')
  parser.add_argument('-e', required=True, dest='edges', help='Output edge file')
  parser.add_argument('-n', required=True, dest='nodes', help='Output node attribute file')
  args = parser.parse_args()
  xmldoc = minidom.parse(args.input)
  node_file = open(args.nodes, 'w')
  edge_file = open(args.edges, 'w')
  nodes = xmldoc.getElementsByTagName('node')
  edges = xmldoc.getElementsByTagName('edge')
  for node in nodes:
    node_id, node_label = node.attributes['id'].value, node.attributes['label'].value
    if node_id != node_label:
      print 'BUG'
      quit()
    attributes = node.getElementsByTagName('attvalues')[0].getElementsByTagName('attvalue')
    for att in attributes:
      if att.attributes['for'].value == '0':
        classname = att.attributes['value'].value
      elif att.attributes['for'].value == '1':
        gender = att.attributes['value'].value
      else:
        print 'BUG'
        quit()
    node_file.write('%s %s %s\n' % (node_id, classname, gender))
  for edge in edges:
    edge_id, source, target = edge.attributes['id'].value, edge.attributes['source'].value, edge.attributes['target'].value,
    attributes = edge.getElementsByTagName('attvalues')[0].getElementsByTagName('attvalue')
    for att in attributes:
      if att.attributes['for'].value == '2':
        duration = att.attributes['value'].value
      elif att.attributes['for'].value == '3':
        count = att.attributes['value'].value
      else:
        print 'BUG'
        quit()
    edge_file.write('%s %s\n' % (source, target))

if __name__ == '__main__':
  main()
