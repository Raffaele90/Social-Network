from Classic_Search.Best_Match.Best_match import *
from Classic_Search.Best_Match.Best_match_optimization import *
from Classic_Search.PageRank.PageRank import *
import time
import csv



def toResultFile(path1, name_result_file, lista,rv):
    with open(path+'Opt_simple.csv', 'w') as csvfile:
        fieldnames = ['Page', 'Best Match', 'Rank']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for doc in lista:
            writer.writerow({'Page': str(doc[0]), 'Best Match': str(doc[1]), 'Rank': str(rv[doc[0]])})
        csvfile.close()

path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"
query = "foNS security"
query = query.lower()
file_graph = open("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/Complete_Graph_Dataset.pickle", "rb")
graph = pickle.load(file_graph)
print("Creazione grafo OK")



''' *** BEST MATCH - PAGE RANK ********* '''
start_time = time.time()
bestmatchTime = time.time()

list_20_docs = best_match(query, 0)
print("Tempo  BEST MATCH --- %s seconds ---" % (time.time() - bestmatchTime))

pageRankTime = time.time()

t,rank = pageRank2(graph,0.85,70,0)
print("Tempo  PAGE RANK --- %s seconds ---" % (time.time() - pageRankTime))

print("--- %s seconds ---" % (time.time() - start_time))
toResultFile(path,"Simple_simple.txt",list_20_docs,rank)




''' ***+++ BEST MATCH OPTIMIZATION - PAGE RANK *********
start_time = time.time()
bestmatchTime = time.time()
list_20_docs = best_match_opt(query, 0)
print("Tempo  BEST MATCH --- %s seconds ---" % (time.time() - bestmatchTime))

pageRankTime = time.time()
t,rank = pageRank2(graph,0.7,70,0)
print("Tempo  PAGE RANK --- %s seconds ---" % (time.time() - pageRankTime))
print("Tempo di esecuzione Best match Opt con PageRank--- %s seconds ---" % (time.time() - start_time))
toResultFile(path,"Opt_simple.txt",list_20_docs,rank)
'''


file_graph.close()
