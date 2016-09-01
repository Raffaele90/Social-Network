from Classic_Search.Best_Match.Best_match import *
from Classic_Search.Best_Match.Best_match_optimization import *
from Classic_Search.PageRank.PageRank import *
from Classic_Search.PageRank.PageRankParallel import *
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
    with open(path1+name_result_file+'.csv', 'w') as csvfile:
        fieldnames = ['Page', 'Best Match', 'Rank']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for doc in lista:
            writer.writerow({'Page': str(doc[0]), 'Best Match': str(doc[1]), 'Rank': str(rv[doc[0]])})
        csvfile.close()


s = 0.85
step = 70
confidence = 0

path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"
query = "google cloud adobe privacy"
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
start_time = timeit.default_timer()
bestmatchTime_simple = timeit.default_timer()
list_20_docs_simple = best_match(query, 0,word_advs,wordsInDoc)
bestmatchTime_simple = timeit.default_timer() - bestmatchTime_simple
print("Tempo  BEST MATCH --- %s seconds ---" % (bestmatchTime_simple))

pageRankTime = timeit.default_timer()
t,rank = pageRank2(graph,s,step,confidence)
elapsed = timeit.default_timer() - pageRankTime
print("Tempo  PAGE RANK --- %s seconds ---" % elapsed)

print("BESTMATCH + PAGE RANK TOT --- %s seconds ---" % (timeit.default_timer() - start_time))
toResultFile(path,"Simple_simple.csv",list_20_docs_simple,rank)


print()

''' ***+++ BEST MATCH OPTIMIZATION - PAGE RANK ********* '''
start_time = timeit.default_timer()
bestmatchTime_opt = timeit.default_timer()
list_20_docs_opt = best_match_opt(query, 0,word_advs,sorted_advs)
bestmatchTime_opt = timeit.default_timer() - bestmatchTime_opt
print("Tempo  BEST MATCH OPT--- %s seconds ---" % (bestmatchTime_opt))

pageRankTime = timeit.default_timer()
t,rank = pageRank2(graph,s,step,confidence)
print("Tempo  PAGE RANK --- %s seconds ---" % (timeit.default_timer() - pageRankTime))
print("BEST MATCH OPT  + PAGE RANK TOT --- %s seconds ---" % (timeit.default_timer() - start_time))
toResultFile(path,"Opt_Simple.csv",list_20_docs_opt,rank)

print()
''' *** BEST MATCH - PAGE RANK PARALLEL ********* '''


degree,simple=create_struct_parallel(graph,4)

start_time = timeit.default_timer()
time, rank = pageRank3(simple, degree, len(graph), s, step, confidence, 16)
elapsed = timeit.default_timer() - start_time

print("BEST MATCH   + PAGE RANK PARALLEL TOT --- %s seconds ---" % (elapsed + bestmatchTime_simple))
path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"

print()

ran = dict()
for r in range(len(rank)):
    dizionario = rank[r]
    for x in dizionario:
        ran[x] = rank[r][x]
toResultFile(path,"Simple_Parallel.csv",list_20_docs_simple,ran)


''' *** BEST MATCH OPT - PAGE RANK PARALLEL ********* '''

degree,simple=create_struct_parallel(graph,4)

start_time = timeit.default_timer()
time, rank = pageRank3(simple, degree, len(graph), s, step, confidence, 16)
elapsed = timeit.default_timer() - start_time

print("BEST MATCH OPT  + PAGE RANK PARALLEL TOT --- %s seconds ---" % (elapsed + bestmatchTime_opt))
path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"

ran = dict()
for r in range(len(rank)):
    dizionario = rank[r]
    for x in dizionario:
        ran[x] = rank[r][x]
toResultFile(path,"Opt_Parallel.csv",list_20_docs_opt,ran)

