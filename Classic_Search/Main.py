from Classic_Search.Best_Match.Best_match import *
from Classic_Search.Best_Match.Best_match_optimization import *
from Classic_Search.PageRank.PageRank import *
import time
import csv


def loadPickle():
    path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"

    if (os.path.isfile(path + "word_advs.pickle") and os.path.isfile(path + "word_in_docs.pickle")):
        file_word_advs = open(path + "word_advs.pickle", "rb")
        word_advs = pickle.load(file_word_advs)

        file_word_in_doc = open(path + "word_in_docs.pickle", "rb")
        wordsInDoc = pickle.load(file_word_in_doc)

        file_word_advs.close()
        file_word_in_doc.close()
    else:
        array = create_word_advs()
        word_advs = array[0]
        wordsInDoc = array[1]

    if (os.path.isfile(path + "Matching_Dataset.pickle")):
        file_matching = open(path + "Matching_Dataset.pickle", "rb")
        sorted_word_advs = pickle.load(file_matching)
    else:
        # ***** Sort di word_advs fatta solo offline *******
        file_matching = open(path + "Matching_Dataset.pickle", "ab+")
        sorted_word_advs = sort_docs(word_advs)
        pickle.dump(sorted_word_advs, file_matching)
        file_matching.close()

    return [word_advs,sorted_word_advs,wordsInDoc]

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
pathPickles = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"
file_graph = open(pathPickles+"Complete_Graph_Dataset.pickle", "rb")
graph = pickle.load(file_graph)
print("Creazione grafo OK")

pickles = loadPickle()

word_advs = pickles[0]
sorted_advs = pickles[1]
wordsInDoc = pickles[2]
print("Pickles Caricarti OK")


''' *** BEST MATCH - PAGE RANK ********* '''
start_time = time.time()
bestmatchTime = time.time()
list_20_docs = best_match(query, 0,word_advs,wordsInDoc)
print("Tempo  BEST MATCH --- %s seconds ---" % (time.time() - bestmatchTime))

pageRankTime = time.time()

t,rank = pageRank2(graph,0.85,70,0)
print("Tempo  PAGE RANK --- %s seconds ---" % (time.time() - pageRankTime))

print("--- %s seconds ---" % (time.time() - start_time))
toResultFile(path,"Simple_simple.txt",list_20_docs,rank)




''' ***+++ BEST MATCH OPTIMIZATION - PAGE RANK *********
start_time = time.time()
bestmatchTime = time.time()
list_20_docs = best_match_opt(query, 0,word_advs,sorted_advs)
print("Tempo  BEST MATCH --- %s seconds ---" % (time.time() - bestmatchTime))

pageRankTime = time.time()
t,rank = pageRank2(graph,0.7,70,0)
print("Tempo  PAGE RANK --- %s seconds ---" % (time.time() - pageRankTime))
print("Tempo di esecuzione Best match Opt con PageRank--- %s seconds ---" % (time.time() - start_time))
toResultFile(path,"Opt_simple.txt",list_20_docs,rank)

'''

