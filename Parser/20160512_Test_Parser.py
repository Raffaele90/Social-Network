#!/usr/bin/python


from lesson5 import read_wibbi

graph,db = read_wibbi("06-2014-text.pages")
for i in graph.keys():
    print(i)
    print(graph[i])
    print(db[i])
    input()