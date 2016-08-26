from Classic_Search.Best_Match.Best_match import *
from Classic_Search.PageRank.PageRank import *
import time



start_time = time.time()

query = "Cleveland Cavaliers NBA result"
query = query.lower()
list_20_docs = best_match(query, 0)


file_graph = open("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/Complete_Graph_Dataset.pickle", "rb")
graph = pickle.load(file_graph)
t,rank = pageRank2(graph,0.95,70,0)


print("--- %s seconds ---" % (time.time() - start_time))
print(list_20_docs)

result_file = open("Results/Simple_Simple.txt",'w')

for doc in list_20_docs:
    toResult = str(doc[0]) +" -- "+str(doc[1]) +" -- "+ str(rank[doc[0]])
    result_file.write(toResult + "\n")