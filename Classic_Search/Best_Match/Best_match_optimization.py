import time
import pickle

#!/usr/bin/python

#The operation of retriving advertisers or documents matching a given query can be executed in two phases:
#in the first phase, we build the necessary data structures;
#in the second phase, we answer to the given query.

#The first phase is usually run only once.
#The data structure that is usually built in this phase is an "inverted index".
#This is a dictionary that for every word (or for every query phrase) mantains a list of
#documents containing that word (query phrase) / advertisers requesting to appear on that word (query phrase).
#In this phase, we assume that there is a database in which we save for each document (advertiser, resp.)
#the link to the document (the name of the advertiser, resp.)
#and the list of word (or phrases) of the document (on which the advertiser request to appear, resp.).
#In the implementations below we assume that the database is a file as follows:
#    nome_adv1 prova,test,prova esame,esame,appello,appello esame
#    nome_adv2 prova,esempio,caso semplice,evidenza
#    nome_adv3 esempio test,esempio esame,esempio prova,esame prova

#The second phase must be executed for any issued query.
#Different strategies are available for this phase:
#either we look for an exact match of the query in the document / advertisers' requests
#or we look for document / advertiser' requests that are "good" match, but not necessarily exact.

###BEST MATCH###

db_path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/db_Best_Match.txt"
limit = 20
#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
def create_word_advs():
    infile = open(db_path)
    word_advs = dict()

    wordsInDoc = dict()
    for line in infile:
        name_list = line.split(' ',1)
        name=name_list[0]
        queries=name_list[1].split(',')
        length = len(queries)


        for i in range(len(queries)):

            query_words=queries[i].split()
            length = length + len(query_words)-1
            for word in query_words:

                if word not in word_advs.keys():
                    word_advs[word]=dict() #We use a set for avoid repetitions
                    ((word_advs[word])[name]) = list()
                    ((word_advs[word])[name]).append(1)
                else:
                    if name not in (word_advs[word]).keys():
                        ((word_advs[word])[name]) = list()
                        ((word_advs[word])[name]).append(1)
                    else:
                        ((word_advs[word])[name])[0] += 1

        wordsInDoc[name] = length


                    #It would be possible to save not only the name but also the occurrence of the word in the document / advertiser's request.
                    #In this case, we need to associate each name with an accumulator that counts the number of occurrence of the words.

    word_advs = calculate_frequency(word_advs,wordsInDoc)
    return [word_advs,wordsInDoc]


def best_match(query, threshold):
    path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Best_Match"
    adv_weights = dict()
    best_docs = set()
    start_time = time.time()
    array = create_word_advs()
    print("CREATE_WORD --- %s seconds ---" % (time.time() - start_time))
    impact = list()
    word_advs = array[0]
    wordsInDoc = array[1]



    # ***** Sort di word_advs fatta solo offline *******

    sorted_word_advs = sort_docs(word_advs)
    file_matching = open(path + "Matching_Dataset.pickle", "ab+")
    pickle.dump(sorted_word_advs,file_matching)
    file_matching.close()

    # *****

    #file_matching = open(path + "Matching_Dataset.pickle", "rb")
    #sorted_word_advs = pickle.load(file_matching)


    print("Sort_Docs --- %s seconds ---" % (time.time() - start_time))
    query_words = query.split()

    print("SPLIT --- %s seconds ---" % (time.time() - start_time))

    #Calcolo impatto di ogni parola della query
    for word in query_words:
        impact = insert_sorted(impact,word,((sorted_word_advs[word])[0])[1])
    print(impact)
    print("IMPACT --- %s seconds ---" % (time.time() - start_time))
    global limit

    dict_20_docs = dict()
    list_word_scored = list()
    list_word_no_scored = list()
    count_docs = 0
    current_doc_index = 0
    for word in query_words:
        if count_docs < limit:
            list_word_scored.append(word)
            current_doc_index = 0

            for doc in sorted_word_advs[word]:
                if doc[0] in dict_20_docs:
                    current_doc_index +=1
                else:
                    dict_20_docs[doc[0]] = doc[1]
                    count_docs +=1
                    current_doc_index +=1
                    if count_docs >= limit:
                        if current_doc_index < len(sorted_word_advs[word]): # Ho ancora documenti ????
                            #list_word_scored.remove(word)
                            to_eliminate = word
                            list_word_no_scored.append(word)
                            break # Ho raggiunto i 20 e devo uscire
                        else: # Ho visto tutti i documenti di word in sorted_word
                            current_doc_index = 0
        else:
            list_word_no_scored.append(word)

    list_20_docs = list()
    for doc in dict_20_docs:
        list_20_docs = insert_doc_1(doc,dict_20_docs[doc],list_20_docs)
        adv_weights[doc] = dict_20_docs[doc]

    # Punto 5 mi calcolo lo score dei 20 documenti su tutte le parole query
    for doc in list_20_docs:
        d = doc[0]
        adv_weights = score_doc(d, query_words, adv_weights, word_advs)

    list_20_docs.clear()
    for doc in adv_weights:
        list_20_docs = insert_doc_1(doc,adv_weights[doc],list_20_docs)


    #Punto 5 mi calcolo lo score dei 20 documenti solo sulle parole scored
    ''' for doc in list_20_docs:
        d = doc[0]
        adv_weights = score_doc(d, list_word_scored, adv_weights, word_advs)'''

    list_word_scored.remove(to_eliminate)
    #Punto 6,7
    index = 0
    for word in list_word_no_scored:
        list_word_scored.append(word) # Aggiungo la nuova parola alla lista delle scored
        for i in range(current_doc_index,len(sorted_word_advs[word])):
            docss = (sorted_word_advs[word])[i] # Primo documento per cui bisogna fare lo score
            ds = docss[0]
            if (docss[0] not in adv_weights): # Non è uno dei migliori 20 ???
                freq_doc_no_scored = ((sorted_word_advs[word])[i])[1]
                # Punto 8
                sum_impact = 0
                index = 0
                # Per ogni termine non scored mi calcolo la somma degli impatti
                for j in range(index, len(list_word_no_scored)):
                    sum_impact += get_impact(list_word_no_scored[j], impact)

                freq_doc_no_scored += sum_impact
                freq_doc_x = (list_20_docs[-1])[1]
                if freq_doc_no_scored > freq_doc_x: # Il 20esimo è meno pesante di quello che sta per entrare ?
                    doc20 = list_20_docs.pop()
                    del adv_weights[doc20[0]]
                    #adv_weights = score_doc(ds, list_word_scored, adv_weights, word_advs)
                    adv_weights[ds] = 0
                    adv_weights = score_doc(ds, query_words, adv_weights, word_advs)
                    docss[1] = adv_weights[docss[0]]
                    list_20_docs = insert_doc(docss,list_20_docs)



        current_doc_index = 0
        list_word_no_scored.remove(word)


    for doc in adv_weights:
        if adv_weights[doc] >= threshold:
           best_docs.add(doc)

    for d in list_20_docs:
        print(d)

    for d in adv_weights:
        print(d)
        print(adv_weights[d])

    return best_docs


def score_doc (document,lws, adv_weights, word_advs):
    for word in lws:
        if document in word_advs[word]:
            if document in adv_weights.keys():
                adv_weights[document] += ((word_advs[word])[document])[0]
    return adv_weights

def insert_sorted (impact, word, freq):
    start_time1 = time.time()
    l = list()
    l.append(word)
    l.append(freq)
    for i in range(len(impact)):
        if ((impact[i])[1] < freq):
            impact.insert(i,l)
            return impact
    impact.append(l)
    print("IMPACT_FUNCTION--- %s seconds ---" % (time.time() - start_time1))
    return  impact


def get_impact(word,impact):
    for i in range(len(impact)):
        if (word == (impact[i])[0]):
            return (impact[i])[1]

def calculate_frequency(word_advs, wordsInDoc):

    for word in word_advs:
        for doc in word_advs[word]:
            ((word_advs[word])[doc])[0] /= wordsInDoc[doc]
    return word_advs


def sort_docs (word_advs):
    sorted_w = dict()
    count = 0
    for word in word_advs:
        if word not in sorted_w:
            sorted_w[word] = list()
        for doc in word_advs[word]:
            sorted_w[word] = insert_sort_list(sorted_w[word],doc,((word_advs[word])[doc])[0])
            count +=1+len(sorted_w[word])
    return sorted_w





def insert_sort_list (lista,doc,freq):
    l = list()
    l.append(doc)
    l.append(freq)
    if (len(lista) == 0):

        lista.append(l)
        return lista

    for i in range(len(lista)):
        f = (lista[i])[1]
        if (freq > f):

            lista.insert(i,l)
            return lista

    lista.append(l)
    return lista


def insert_doc(doc,l):

    for i in range(0,len(l)):
        if ((l[i])[1] < doc[1]):
            l.insert(i,doc)
            return l

    l.append(doc)
    return l

def insert_doc_1(key,value,l):
    lista_fons = list()
    lista_fons.append(key)
    lista_fons.append(value)
    for i in range(0,len(l)):
        if ((l[i])[1] < value):

            l.insert(i,lista_fons)
            return l

    l.append(lista_fons)
    return l

#create_word_advs()
#path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Best_Match"

#start_time = time.time()
#list_docs = best_match("Facebook Twitter information",0)
#print("--- %s seconds ---" % (time.time() - start_time))
#print(list_docs)
#set2 = exact_match("prova esame")
#print(set)
#print(set2)




