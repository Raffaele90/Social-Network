from Classic_Search.Best_Match.Best_match import *
from Classic_Search.Best_Match.Best_match_optimization import *
from Classic_Search.PageRank.PageRankParallel import *
from Classic_Search.TopicSensitive.TopicSensitivePageRank import *
import time
import csv
from re import sub

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


def toResultFile(path1, name_result_file, lista,rv,bm,ranking,time_bm,time_ranking):
    with open(path1+name_result_file+'.csv', 'w') as csvfile:

        fieldnames = ['Query']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Query': query})

        writer.writerow({'Query': " "})

        fieldnames = ['Page', 'Best Match', 'Rank','T_'+bm,'T_'+ranking,'Tot_Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for doc in lista:
            val_bm = doc[1] * 100
            val_bm = sub(r'\.', ',', str(val_bm))
            val_bm = sub(r'e', 'E', val_bm)

            val_rank = rv[doc[0]] * 10000
            val_rank = sub(r'\.', ',', str(val_rank))
            val_rank = sub(r'e', 'E', val_rank)
            writer.writerow({'Page': str(doc[0]), 'Best Match': val_bm, 'Rank': val_rank})

        writer.writerow({'Page': "", 'Best Match': "", 'Rank': "",'T_'+bm: str(time_bm), 'T_'+ranking: str(time_ranking),'Tot_Time': str(time_bm+time_ranking)})



        diz = dict()
        fieldnames2 = []
        for q in query.split(" "):
            fieldnames2.append(q)
            if q not in diz:
                diz[q] = list()
            l = sorted_advs[q]
            for i in l:
                diz[q].append(i)

        #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #writer.writeheader()
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(list(diz.keys()))
        # now data, assuming each column has the same # of values
        for i in range(20):
            csvWriter.writerow([diz[k][i] for k in diz.keys()])


            #    writer = csv.writer(csvfile)
            #   for key, value in diz.items():
            #        writer.writerow([key, value])

        csvfile.close()



def run_classic_search(bm,ranking,query,num_query):

    print((bm+" "+ranking).upper())
    bestmatchTime = timeit.default_timer()
    if (bm == "best_match"):
        list_20_docs = best_match(query, 0, word_advs, wordsInDoc)
    elif bm == "best_match_opt":
        list_20_docs = best_match_opt(query, 0,word_advs,sorted_advs)
    bestmatchTime_elapsed = timeit.default_timer() - bestmatchTime
    print("Tempo "+bm+" --- %s seconds ---" % (bestmatchTime_elapsed))


    degree, simple = create_struct_parallel(graph, 4)
    rankingTime = timeit.default_timer()
    if ranking == "page_rank":
        t, rank = pageRank2(graph, s, step, confidence)
    elif ranking == "page_rank_parallel":
        t, rank = pageRank3(simple, degree, len(graph), s, step, confidence, 16)

    elif ranking == "topic_sensitive":
        #t, rank = topicSensitiveRanking(graph, s, step, confidence, query, categories_graph, top_words)
        t, rank, no_use = topicSensitiveRanking(graph, s, step, confidence, query, categories_graph, top_words,word_X_cat)

    elif ranking == "topic_sensitive_parallel":
        t, rank = topic_sensitive_parallel(simple,graph, degree, len(graph), s, step, confidence, 16,categories_graph,top_words,word_X_cat,query)

    rankingelapsed = timeit.default_timer() - rankingTime
    print("Tempo "+ranking+"  --- %s seconds ---" % rankingelapsed)
    print("Tempo "+bm+ " + " + ranking + "  --- %s seconds ---" + str(bestmatchTime_elapsed+rankingelapsed))


    path_result ="/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"
    if not os.path.exists(path_result+"query"+num_query):
        os.makedirs(path_result+"query"+num_query)

    path_result = path_result+"query"+num_query+"/"
    if (ranking == "page_rank_parallel") or (ranking == "topic_sensitive_parallel"):
        ran = dict()
        for r in range(len(rank)):
            dizionario = rank[r]
            for x in dizionario:
                ran[x] = rank[r][x]
        toResultFile(path_result, bm+" "+ranking, list_20_docs, ran,bm,ranking,bestmatchTime_elapsed,rankingelapsed)
    else:
        print()
        toResultFile(path_result, bm+ranking, list_20_docs, rank,bm,ranking,bestmatchTime_elapsed,rankingelapsed)
    #time.sleep(5)
    print()










s = 0.85
step = 70
confidence = 0

path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Results/"
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
print("Pickles Caricarti OK")

queries=["drugs medicine","nba sports","health medicine food","information security facebook twitter","science videos"]
size =len(queries)
toRemove = []
for query in queries:
    #query = queries[i]
    words = query.split(" ")
    for word in words:
        word = word.lower()
        if word not in word_X_cat:
            #queries.remove(query)
            toRemove.append(query)
            print("Non posso estrapolare topic per la parola " + word)
            #print("La query '" + query + "' non verrà eseguita")
            break

for query in toRemove:
    queries.remove(query)
    print("La query '" + query + "' non verrà eseguita")

for i in range(len(queries)):
    query = queries[i]
    query = query.lower()
    num_query = str(i)

    print()
    print()
    print("**** Query "+num_query+" ****")
    print()
    run_classic_search("best_match","page_rank",query,num_query)

    """
    run_classic_search("best_match", "page_rank_parallel", query,num_query)
    run_classic_search("best_match_opt", "page_rank", query,num_query)
    run_classic_search("best_match_opt", "page_rank_parallel", query,num_query)
    run_classic_search("best_match", "topic_sensitive", query,num_query)
    #run_classic_search("best_match", "topic_sensitive_parallel", query,num_query)
    run_classic_search("best_match_opt", "topic_sensitive", query,num_query)
    #run_classic_search("best_match_opt", "topic_sensitive_parallel", query,num_query)
"""

"""
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

print()

''' *** BEST MATCH - TOPIC SENSITIVE ********* '''
start_time = timeit.default_timer()
bestmatchTime_simple = timeit.default_timer()
list_20_docs_simple = best_match(query, 0,word_advs,wordsInDoc)
bestmatchTime_simple = timeit.default_timer() - bestmatchTime_simple
print("Tempo  BEST MATCH --- %s seconds ---" % (bestmatchTime_simple))

topicsensitiveTime = timeit.default_timer()
t,rank = topicSensitiveRanking(graph,s,step,confidence,query,categories_graph,top_words)
elapsed = timeit.default_timer() - topicsensitiveTime
print("Tempo  Topic Sensitive --- %s seconds ---" % elapsed)

print("BESTMATCH + TOPIC SENSITIVE TOT --- %s seconds ---" % (timeit.default_timer() - start_time))
toResultFile(path,"Simple_sensitive.csv",list_20_docs_simple,rank)


print()

"""