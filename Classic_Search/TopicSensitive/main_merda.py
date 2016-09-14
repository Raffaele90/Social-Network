from Classic_Search.Best_Match.Best_match import *
from Classic_Search.Best_Match.Best_match_optimization import *
from Classic_Search.PageRank.PageRank import *
from Classic_Search.PageRank.PageRankParallel import *
from Classic_Search.TopicSensitive.TopicSensitivePageRank import *

import time
import csv

def toResultFile(path1, name_result_file, lista,rv,categories_graph):
    with open(path1+name_result_file+'.csv', 'w') as csvfile:
        fieldnames = ['Page', 'Category', 'Best Match', 'Rank']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        category = ""
        for doc in lista:
            for cat in categories_graph.keys():
                if doc[0] in categories_graph[cat].keys():
                    category +="-"+cat
            writer.writerow({'Page': str(doc[0]), 'Category': str(category), 'Best Match': str(doc[1]), 'Rank': str(rv[doc[0]])})
            category=""
        csvfile.close()

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
    if (os.path.isfile(path + "Categories_Graph.pickle")):
        file_categories =  open(path + "Categories_Graph.pickle", "rb")
        categories_graph = pickle.load(file_categories)
        file_top_words = open(path + "Top_Words.pickle", "rb")
        pick_words = pickle.load(file_top_words)

        file_categories.close()
        file_top_words.close()

    return [word_advs,sorted_word_advs,wordsInDoc,categories_graph,pick_words]


s = 0.85
step = 70
confidence = 0

path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"
query = "sports college"#"search video digital"   #""business health home"
query = query.lower()
pathPickles = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"
file_graph = open(pathPickles+"Complete_Graph_Dataset.pickle", "rb")
graph = pickle.load(file_graph)
print("Creazione grafo OK")



pickles = loadPickle()

word_advs = pickles[0]
sorted_advs = pickles[1]
wordsInDoc = pickles[2]
categories_graph=pickles[3]
top_words = pickles[4]

word_X_cat = dict()
for cat in top_words:
    for w in top_words[cat]:
        if w in word_X_cat:
            word_X_cat[w].add(cat)
        else:
            word_X_cat[w] = set()
            word_X_cat[w].add(cat)


for w in word_X_cat:
    if len(word_X_cat[w]) == 1:
        #vari = "Kids"
    #if (vari in word_X_cat[w]):
        print("Parola "+w)
        print("Trovata nelle cat: "+str(word_X_cat[w]))

print("Pickles Caricarti OK")

''' *** BEST MATCH - TOPIC SENSITIVE ********* '''
start_time = timeit.default_timer()
bestmatchTime_simple = timeit.default_timer()
list_20_docs_simple = best_match(query, 0,word_advs,wordsInDoc)
bestmatchTime_simple = timeit.default_timer() - bestmatchTime_simple
print("Tempo  BEST MATCH --- %s seconds ---" % (bestmatchTime_simple))

topicsensitiveTime = timeit.default_timer()
t,rank,no_use = topicSensitiveRanking(graph,s,step,confidence,query,categories_graph,top_words,word_X_cat)
elapsed = timeit.default_timer() - topicsensitiveTime
print("Tempo  Topic Sensitive --- %s seconds ---" % elapsed)

print("BESTMATCH + Topic Sensitive TOT --- %s seconds ---" % (timeit.default_timer() - start_time))
toResultFile(path,"Simple_sensitive.csv",list_20_docs_simple,rank,categories_graph)


print()


''' *** BEST MATCH OPT - TOPIC SENSITIVE ********* '''
start_time = timeit.default_timer()
bestmatchTime_simple = timeit.default_timer()
list_20_docs_simple = best_match_opt(query, 0,word_advs,sorted_advs)
bestmatchTime_simple = timeit.default_timer() - bestmatchTime_simple
print("Tempo  BEST MATCH OPT --- %s seconds ---" % (bestmatchTime_simple))

topicsensitiveTime = timeit.default_timer()
t,rank,no_use = topicSensitiveRanking(graph,s,step,confidence,query,categories_graph,top_words,word_X_cat)
elapsed = timeit.default_timer() - topicsensitiveTime
print("Tempo  Topic Sensitive --- %s seconds ---" % elapsed)

print("BESTMATCH_OPT + Topic Sensitive TOT --- %s seconds ---" % (timeit.default_timer() - start_time))
toResultFile(path,"Opt_sensitive.csv",list_20_docs_simple,rank,categories_graph)


print()