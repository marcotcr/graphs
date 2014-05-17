#include "graph.h"
#include <cstdio>
#include <cstdlib>
#include <cassert>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <queue>
#include <random>
using std::vector;
using std::string;
using std::sort;
using std::unordered_set;
using std::queue;
using std::unordered_map;
Graph::Graph() {
  complement_ = NULL;
}
Graph::Graph(std::string edge_file) {
  FILE* file = fopen(edge_file.c_str(), "r");
  assert(file != NULL);
  int node1, node2;
  while (fscanf(file, "%d %d", &node1, &node2) == 2) {
    graph_[node1][node2] = true;
    graph_[node2][node1] = true;
  }
  complement_ = NULL;
}
Graph::Graph(const std::unordered_map<int, std::unordered_map<int, bool> > graph):
  graph_(graph) { 
  complement_ = NULL;
}
Graph::Graph(const Graph& graph, const std::vector<int>& nodes) {
  int node1, node2;
  std::unordered_map<int, std::unordered_map<int, bool> > complement;
  for (int i = 0; i < nodes.size(); ++i) {
    node1 = nodes[i];
    graph_[node1].size();
    complement[node1].size();

    for (int j = i + 1; j < nodes.size(); ++j) {
      node2 = nodes[j];
      if (graph.HasEdge(node1, node2)) {
        graph_[node1][node2] = true;
        graph_[node2][node1] = true;
      }
      else {
        complement[node1][node2] = true;
        complement[node2][node1] = true;
      }
    }
  }
  complement_ = new Graph(complement);
  nodes_ = nodes;
}
Graph::~Graph() {
  if (complement_) {
    delete complement_;
  }
}

bool Graph::HasEdge(int i, int j) const {
  auto find_i = graph_.find(i);
  if (find_i != graph_.end()) {
    auto find_j = find_i->second.find(j);
    if (find_j != find_i->second.end()) {
      return find_j->second;
    }
  }
  return false;
}

std::string Graph::DegreeDistribution() {
  int n = graph_.size();
  vector<int> degrees(n);
  int i = 0;
  for (auto node : graph_) {
    degrees[i++] = node.second.size();
  }
  sort(degrees.begin(), degrees.end());
  string answer;
  answer.resize(n);
  for (int j = 0; j < n; ++j) {
    answer[j] = degrees[j] + 48;
  }
  if (complement_) {
    answer += "_" + complement_->DegreeDistribution();
  }
  return answer;
}

std::string Graph::ConnectedComponents() {
  vector<int> sizes;
  unordered_set<int> nodes;
  queue<int> Q;
  for (auto i: graph_) {
    nodes.insert(i.first);
  }
  while (!nodes.empty()) {
    int x = *(nodes.begin());
    Q.push(x);
    nodes.erase(x);
    int size_cc = 0;
    while (!Q.empty()) {
      x = Q.front();
      Q.pop();
      size_cc++;
      for (auto y: graph_[x]) {
        if (nodes.find(y.first) != nodes.end()) {
          nodes.erase(y.first);
          Q.push(y.first);
        }
      }
    }
    sizes.push_back(size_cc);
  }
  sort(sizes.begin(), sizes.end());
  string answer;
  int n = sizes.size();
  answer.resize(n);
  for (int j = 0; j < n; ++j) {
    answer[j] = sizes[j] + 48;
  }
  if (complement_) {
    answer += "_" + complement_->ConnectedComponents();
  }
  return answer;
}
std::string Graph::Bipartite() {
  unordered_set<int> nodes;
  queue<int> Q;
  for (auto i: graph_) {
    nodes.insert(i.first);
  }
  unordered_map<int, int> colors;
  int bipartite = 1;
  while (!nodes.empty()) {
    int x = *(nodes.begin());
    Q.push(x);
    nodes.erase(x);
    colors[x] = 0;
    while (!Q.empty()) {
      x = Q.front();
      Q.pop();
      for (auto y: graph_[x]) {
        if (colors.find(y.first) != colors.end()) {
          if (colors[y.first] == colors[x]) {
            bipartite = 0;
            while (!Q.empty()) {
              Q.pop();
            }
            nodes.clear();
            break;
          }
        } else {
            if (colors[x] == 0) 
              colors[y.first] = 1;
            else
              colors[y.first] = 0;
        }
        if (nodes.find(y.first) != nodes.end()) {
          nodes.erase(y.first);
          Q.push(y.first);
        }
      }
    }
  }
  string answer("0");
  answer[0] = bipartite + 48;
  if (complement_) {
    answer += "_" + complement_->Bipartite();
  }
  return answer;
}
int Graph::LSP(int node) {
  queue<int> Q;
  Q.push(node);
  unordered_map<int, int> distances;
  for (auto i: graph_) {
    distances[i.first] = 9;
  }
  distances[node] = 0;
  unordered_set<int> visited;
  visited.insert(node);
  while (!Q.empty()) {
    int x = Q.front();
    Q.pop();
    for (auto y: graph_[x]) {
      if (visited.find(y.first) == visited.end()) {
        distances[y.first] = distances[x] + 1;
        Q.push(y.first);
        visited.insert(y.first);
      }
    }
  }
  int max_distance = 0;
  for (auto x: distances) {
    if (x.second > max_distance) {
      max_distance = x.second;
    }
  }
  return max_distance;
}
std::string Graph::LSPDistribution() {
  int n = graph_.size();
  vector<int> lsps(n);
  int i = 0;
  for (auto x: graph_) {
    lsps[i++] = LSP(x.first);
  }
  sort(lsps.begin(), lsps.end());
  string answer;
  answer.resize(n);
  for (int j = 0; j < n; ++j) {
    answer[j] = lsps[j] + 48;
  }
  if (complement_) {
    answer += "_" + complement_->LSPDistribution();
  }
  return answer;
}
std::string Graph::Canonical() {
  string answer = "DD:" + DegreeDistribution() + ",";
  answer += "CC:" + ConnectedComponents() + ",";
  answer += "B:" + Bipartite() + ",";
  answer += "LSP:" + LSPDistribution();
  return answer;
}
Graph Graph::Egonet(int node) {
  std::vector<int> nodes;
  assert(graph_.find(node) != graph_.end());
  for (auto x: graph_[node]) {
    nodes.push_back(x.first);
  }
  Graph g(*this, nodes);
  return g;
}

Graph Graph::Binet(int node1, int node2) {
  std::vector<int> nodes;
  assert(graph_.find(node1) != graph_.end());
  assert(graph_.find(node2) != graph_.end());
  assert(graph_[node1].find(node2) != graph_[node1].end());
  std::unordered_set<int> unique;
  for (auto x: graph_[node1]) {
    unique.insert(x.first);
  }
  for (auto x: graph_[node2]) {
    unique.insert(x.first);
  }
  unique.erase(node1);
  unique.erase(node2);
  for (auto x: unique) {
    nodes.push_back(x);
  }
  Graph g(*this, nodes);
  return g;
}
std::unordered_map<std::string, int> Graph::SampleSubgraphs(int n_subgraphs, int size) { 
  std::random_device device;
  std::mt19937 generator(device());
  vector<int> nodes(size);
  unordered_map<string, int> result;
  for (int z = 0; z < n_subgraphs; ++z) {
    std::shuffle(nodes_.begin(), nodes_.end(), generator);
    std::copy(nodes_.begin(), nodes_.begin() + size, nodes.begin());
    Graph subgraph(*this, nodes);
    result[subgraph.Canonical()]++;
  }
  return result;
}
