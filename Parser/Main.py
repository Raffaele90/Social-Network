#Crea:
# out_file è il db che servirà a Best match
# Creazione del grafo per Page Rank

from Parser.Impl_Parser import *
from Classic_Search.PageRank.Graph import *
import os
import pickle


graph_path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/Ranking_Dataset.pickle"

db_path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/db_Best_Match.txt"


out_file = open(db_path,"w")
file_parsed  = open(graph_path, "ab+")

path = os.getcwd()
print(path)
pathdataset = path+"/datasetRS"

graph_merge = list()

for i in os.listdir(pathdataset):
    if i.endswith(".pages"):
        path = pathdataset + "/" + i
        graph, db = read_wibbi(path)
        graph_merge.append(graph)

    for i in graph.keys():
        if (len(db[i]) != 0):
            str = i +" "
            for line in db[i]:
              str += line.lower()+","

            out_file.write(str[:-1]+"\n")

pickle.dump(graph_merge,file_parsed)
file_parsed.close()
out_file.close()


# Creazione del grafo
create_complete_graph("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/",False)
