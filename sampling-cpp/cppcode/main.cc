#include "graph.h"
#include <iostream>
#include <cassert>
#include <cstdio>
using namespace std;

int PossibleSubgraphs(int size) {
  if (size == 3) {
    return 4;
  }
  if (size == 4) {
    return 11;
  }
  if (size == 5) {
    return 34;
  }
  if (size == 6) {
    return 156;
  }
  if (size == 7) {
    return 820;
  }
  return 0;
}
int main(int argc, char** argv) {
  if (argc != 6) {
    printf("Usage:\n");
    printf("edges binet_edges n_samples subgraph_size output_data\n");
    exit(0);
  }
  Graph big_graph(argv[1]);
  FILE* binet_edges = fopen(argv[2], "r");
  assert(binet_edges != NULL);
  int n_samples = atoi(argv[3]);
  assert(n_samples != 0);
  int subgraph_size = atoi(argv[4]);
  assert(subgraph_size != 0);
  FILE* output_file = fopen(argv[5], "w");
  vector<pair<int, int> > binets;
  int node1, node2;
  while (fscanf(binet_edges, "%d %d", &node1, &node2) == 2) {
    binets.push_back(make_pair(node1, node2));
  }
  vector<unordered_map<string, int> > reps(binets.size());
  int count = 0;
  #pragma omp parallel for
  for (unsigned int i = 0; i < binets.size(); ++i) {
    Graph binet = big_graph.Binet(binets[i].first, binets[i].second);
    reps[i] = binet.SampleSubgraphs(n_samples, subgraph_size);
    count++;
    if (count % 100 == 0) {
      printf("Processed %d graphs.\n", count);
    }
  }

  int possible_subgraphs = PossibleSubgraphs(subgraph_size);
  int feature_count = 0;
  unordered_map<string, int> feature_id;
  vector<int> temp;
  for (unsigned int i = 0; i < reps.size(); ++i) {
    temp.clear();
    temp.resize(possible_subgraphs);
    for (auto x: reps[i]) {
      if (feature_id.find(x.first) == feature_id.end()) {
        feature_id[x.first] = feature_count++;
      }
      temp[feature_id[x.first]] = x.second;
    }
    for (auto x: temp) {
      fprintf(output_file, "%d ", x);
    }
    fprintf(output_file, "\n");
  }
  fclose(output_file);
  return 0;
}
