#ifndef GRAPH_H
#define GRAPH_H
#include <string>
#include <vector>
#include <unordered_map>
class Graph {
 public:
  Graph();
  ~Graph();
  // Default constructor.
  Graph(std::string edge_file);
  // Constructs a subgraph from a given graph.
  Graph(const Graph& graph, const std::vector<int>& nodes);
  Graph(const std::unordered_map<int, std::unordered_map<int, bool> > graph);
  std::string Canonical();
  // Returns a graph that is composed of all the neighbors of node.
  Graph Egonet(int node);
  // Returns a graph that is the union of the neighbors of both nodes.
  Graph Binet(int node1, int node2);
  std::unordered_map<std::string, int> SampleSubgraphs(int n_subgraphs, int size);
 private:
  bool HasEdge(int i, int j) const;
  // Returns number of neighbors in a string.
  std::string DegreeDistribution();
  // Returns sizes of connected components in a string.
  std::string ConnectedComponents();
  std::string Bipartite();
  std::string LSPDistribution();
  // Longest shortest path starting from node
  int LSP(int node);
  std::unordered_map<int, std::unordered_map<int, bool> > graph_;
  // Only used if second constructor is used.
  Graph* complement_;
  // Only used if second constructor is used.
  std::vector<int> nodes_;
};
#endif 
