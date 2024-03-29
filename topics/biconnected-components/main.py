#! /usr/bin/env python3

# https://www.geeksforgeeks.org/biconnected-components/
from collections import defaultdict
import sys

class Graph:
   def __init__(self, size):
      self.size = size
      self.graph = [[] for _ in range(self.size)]
      self.time = 0
      self.set_articulation = set()
      self.list_bridge = []
      self.list_biconnected = []

   def find_biconnected(self):
      depth = [-1] * (self.size)
      low = [-1] * (self.size)
      parent = [-1] * (self.size)
      stack = []
      for origin in range(self.size):
         if depth[origin] == -1:
            self.explore(origin, parent, low, depth, stack)
         if stack:
            component = set()
            while stack:
               edge = stack.pop()
               component.add(edge[0])
               component.add(edge[1])
            self.list_biconnected.append(component)
            if (len(component) == 2):
               self.list_bridge.append(component)
      self.sort()
 
   def explore(self, u, parent, low, depth, stack):
      number_child = 0
      depth[u] = self.time
      low[u] = self.time
      self.time += 1
      for v in self.graph[u]:
         if depth[v] == -1 :
            parent[v] = u
            number_child += 1
            stack.append((u, v))
            self.explore(v, parent, low, depth, stack)
            low[u] = min(low[u], low[v])
            if (
               (parent[u] == -1 and number_child > 1)
               or (parent[u] != -1 and low[v] >= depth[u])
            ):
               component = set()
               edge = -1
               while edge != (u, v):
                  edge = stack.pop()
                  component.add(edge[0])
                  component.add(edge[1])
               self.list_biconnected.append(component)
               if (len(component) == 2):
                  self.list_bridge.append(component)
               self.set_articulation.add(u)
         elif (v != parent[u] and low[u] > depth[v]):
            low[u] = min(low[u], depth[v])
            stack.append((u, v))

   def sort(self):
      self.set_articulation = sorted(self.set_articulation)
      list_bridge_sorted = []
      for bridge in self.list_bridge:
         list_bridge_sorted.append(sorted(bridge))
      list_bridge_sorted = sorted(list_bridge_sorted, key=lambda x: x[0])
      self.list_bridge = list_bridge_sorted
      list_biconnected_sorted = []
      for biconnected in self.list_biconnected:
         list_biconnected_sorted.append(sorted(biconnected))
      list_biconnected_sorted = sorted(list_biconnected_sorted, key=lambda x: x[0])
      self.list_biconnected = list_biconnected_sorted

   def output(self):
      print("articulation:")
      for vertex in sorted(self.set_articulation):
         print(vertex, end=' ')
      print()
      print("bridge:")
      for bridge in self.list_bridge:
         for vertex in sorted(bridge):
            print(vertex, end=' ')
         print()
      print("biconnected:")
      for biconnected in self.list_biconnected:
         for vertex in sorted(biconnected):
            print(vertex, end=' ')
         print()
  
   def add_edge(self, u, v):
      self.graph[v].append(u) 
      self.graph[u].append(v)

graph = Graph(64)
document = open(sys.argv[1], "r")
content = document.read()
document.close()
for line in content.splitlines():
   many_vertex = line.split()
   text_source = many_vertex[0]
   for text_vertex in many_vertex[1:]:
      graph.add_edge(int(text_source), int(text_vertex))

graph.find_biconnected()
graph.output()