import matplotlib.pyplot as plt
import collections
import numpy as np
unique_pairs = set()
ego_size = {}
unions = []
intersections = []
edges = []
node_gender = {}
gender_sizes = collections.defaultdict(lambda:[])
gender_edges = collections.defaultdict(lambda:[])
for line in open('nodes_day1'):
  node, a, gender = line.strip().split()
  if gender == 'M' or gender == 'F':
    node_gender[node] = gender
  
for line in open('corpus-statistics'):
  users, u1, u2, union, inters, edge = line.strip().split()
  user1, user2 = sorted(users.split('-'))
  gender = ''.join(sorted('%s%s' % (node_gender[user1], node_gender[user2])))
  gender_sizes[gender].append(int(union))
  gender_edges[gender].append(edge)
  if user1+'-'+user2 in unique_pairs:
    print 'BUG'
    quit()
  ego_size[user1] = int(u1)
  ego_size[user2] = int(u2)
  unions.append(int(union))
  intersections.append(int(inters))
  unique_pairs.add(user1+'-'+user2)
  edges.append(edge)

plt.figure()
plt.title('Ego network sizes')
plt.hist(ego_size.values())
plt.xlabel('Sizes')
plt.savefig('ego_sizes.png')

plt.figure()
plt.title('Union sizes')
plt.hist(unions)
plt.savefig('unions.png')

plt.figure()
plt.title('Intersection sizes')
plt.hist(intersections)
plt.savefig('intersections.png')
for gender in gender_sizes:
  print gender, np.mean(gender_sizes[gender]), '+-', np.std(gender_sizes[gender])
