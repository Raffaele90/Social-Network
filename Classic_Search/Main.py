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


def toResultFile(path1, name_result_file, lista,rv,bm,ranking,time_bm,time_ranking,count_docs_analized):
    with open(path1+name_result_file+'.csv', 'w') as csvfile:


        fieldnames = ['Page' , 'Best Match', 'Rank','Category','T_'+bm,'T_'+ranking,'Tot_Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print ("URL \t Rank")
        print("Query")
        for doc in lista:
            val_bm = doc[1]
            val_bm = sub(r'\.', ',', str(val_bm))
            val_bm = sub(r'e', 'E', val_bm)
            category = ""
            val_rank = rv[doc[0]] * 1000000
            val_rank = sub(r'\.', ',', str(val_rank))
            val_rank = sub(r'e', 'E', val_rank)

            for cat in categories_graph.keys():
                if doc[0] in categories_graph[cat].keys():
                    category +="-"+cat
            print(str(doc[0]) + " \t " + str(val_rank)+" \t "+category)
            writer.writerow({'Page': str(doc[0]), 'Best Match': val_bm, 'Rank': val_rank, 'Category': category})

        writer.writerow({'Page': "", 'Category': "" , 'Best Match': "", 'Rank': "",'T_'+bm: str(time_bm), 'T_'+ranking: str(time_ranking),'Tot_Time': str(time_bm+time_ranking)})
        writer.writerow({'Best Match': "Docs_analized "+str(count_docs_analized)})


        csvfile.close()

    with open(path1 + name_result_file + '_query_freq.csv', 'w') as csvfile:

        diz = dict()
        fieldnames2 = []
        for q in query.split(" "):
            fieldnames2.append(q)
            if q not in diz:
                diz[q] = list()
            l = sorted_advs[q]
            for i in l:
                diz[q].append(i)


        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(list(diz.keys()))
        # now data, assuming each column has the same # of values
        for i in range(20):
            csvWriter.writerow([diz[k][i] for k in diz.keys()])

        fieldnames = ['Query']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'Query': query})
        csvfile.close()


def run_classic_search(bm,ranking,query,num_query):

    list_20_docs = list()
    print((bm+" "+ranking).upper())
    bestmatchTime = timeit.default_timer()
    if (bm == "best_match"):
        list_20_docs.clear()
        cont_docs_anlized,list_20_docs = best_match(query, 0, word_advs, wordsInDoc)
    elif bm == "best_match_opt":
        list_20_docs.clear()
        cont_docs_anlized,list_20_docs = best_match_opt(query, 0,word_advs,sorted_advs,wordsInDoc)
    bestmatchTime_elapsed = timeit.default_timer() - bestmatchTime
    print("Tempo "+bm+" --- %s seconds ---" % (bestmatchTime_elapsed))


    degree, simple = create_struct_parallel(graph, 2)
    rankingTime = timeit.default_timer()
    if ranking == "page_rank":
        t, rank = pageRank2(graph, s, step, confidence)
    elif ranking == "page_rank_parallel":
        t, rank = pageRank3(simple, degree, len(graph), s, step, confidence, 4)

    elif ranking == "topic_sensitive":
        #t, rank = topicSensitiveRanking(graph, s, step, confidence, query, categories_graph, top_words)
        t, rank, no_use = topicSensitiveRanking(graph, s, step, confidence, query, categories_graph, top_words,word_X_cat)

    elif ranking == "topic_sensitive_parallel":
        t, rank = topic_sensitive_parallel(simple,graph, degree, len(graph), s, step, confidence, 4,categories_graph,top_words,word_X_cat,query)

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
        toResultFile(path_result, bm+" "+ranking, list_20_docs, ran,bm,ranking,bestmatchTime_elapsed,rankingelapsed,cont_docs_anlized)
    else:
        print()
        toResultFile(path_result, bm+ranking, list_20_docs, rank,bm,ranking,bestmatchTime_elapsed,rankingelapsed,cont_docs_anlized)
    #time.sleep(5)
    print()

    print("Query: "+query)






def stampa_wort_per_frequenza(namefile,min,max,sorted_advs):
    path1="/Users/raffaeleschiavone/PycharmProjects/Social-Network/"
    with open(path1 +  namefile + '.csv', 'w') as csvfile:
        fieldnames = ['Word', 'Impatto', 'N_Docs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for word in sorted_advs:
            app = sorted_advs[word][0]


            if app[1] > min and sorted_advs[word][0][1] < max:

                writer.writerow({'Word':word, 'Impatto':str(sorted_advs[word][0][1]),'N_Docs':str(len(sorted_advs[word]))})

    csvfile.close()

s = 0.85
step = 75
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


#stampa_wort_per_frequenza("word_0.1_0.9",0.001,0.04,sorted_advs)

#stampa_wort_per_frequenza("word_0.5_1.0",0.05,0.1,sorted_advs)
#stampa_wort_per_frequenza("word_1.0_2.0",0.1,0.2,sorted_advs)
#stampa_wort_per_frequenza("word_2.0_3.0",0.2,0.3,sorted_advs)
#stampa_wort_per_frequenza("word_3.0_5.0",0.3,0.5,sorted_advs)




word_X_cat = dict()
for cat in top_words:
    for w in top_words[cat]:
        if w in word_X_cat:
            word_X_cat[w].add(cat)
        else:
            word_X_cat[w] = set()
            word_X_cat[w].add(cat)


wordssss = "hoteles hotel booking.com hotels fons click"
for wordss in wordssss.split(" "):
    print(wordss)
    print(word_X_cat[wordss])


print("Pickles Caricarti OK")

#Query 0 = 2Top 2Center 2Low  "page - news us link information"
#Query 1 = 2Top 4Center       "company page new best sports 2014"
#Query 2 = 7 low              "information link 2014 latest account network hit"
#Query 3 = 7 Top              "company nba google - directv mtv squad"
#Query 4 = 3 Top              "&#160 href= -"
#Query 5 = 1Top 1Center 1Low  "- video information"
#Query 6 = 3 Top 5Low         ". news href= - svenska ratings informationthe wherever bundle"

queries =["google nba players"]
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

    #run_classic_search("best_match", "page_rank", query, num_query)
    #run_classic_search("best_match_opt", "page_rank", query, num_query)

    #run_classic_search("best_match", "page_rank_parallel", query,num_query)
    #run_classic_search("best_match_opt", "page_rank_parallel", query,num_query)
    run_classic_search("best_match", "topic_sensitive", query,num_query)
    run_classic_search("best_match", "topic_sensitive_parallel", query,num_query)
    #run_classic_search("best_match_opt", "topic_sensitive", query,num_query)
    #run_classic_search("best_match_opt", "topic_sensitive_parallel", query,num_query)

