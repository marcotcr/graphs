#include "graph.h"
#include <iostream>
#include <cassert>
#include <cstdio>
using namespace std;

int main(int argc, char** argv) {
  if (argc != 4) {
    printf("Usage:\n");
    printf("edges binet_edges output_data\n");
    exit(0);
  }
  Graph big_graph(argv[1]);
  FILE* binet_edges = fopen(argv[2], "r");
  assert(binet_edges != NULL);
  FILE* output_file = fopen(argv[3], "w");
  vector<pair<int, int> > binets;
  int node1, node2;
  while (fscanf(binet_edges, "%d %d", &node1, &node2) == 2) {
    binets.push_back(make_pair(node1, node2));
  }
  vector<string> reps(binets.size());
  int count = 0;
  #pragma omp parallel for
  for (unsigned int i = 0; i < binets.size(); ++i) {
    Graph binet = big_graph.Binet(binets[i].first, binets[i].second);
    reps[i] = binet.KitchenSink();
    count++;
    if (count % 100 == 0) {
      printf("Processed %d graphs.\n", count);
    }
  }

  for (unsigned int i = 0; i < reps.size(); ++i) {
    fprintf(output_file, "%s\n", reps[i].c_str());
  }
  fclose(output_file);
  return 0;
}
