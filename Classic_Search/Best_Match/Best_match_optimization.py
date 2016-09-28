import time
import pickle
import timeit
import os

#!/usr/bin/python

#The operation of retriving advertisers or documents matching a given query can be executed in two phases:
#in the first phase, we build the necessary data structures;
#in the second phase, we answer to the given query.

#The first phase is usually run only once.
#The data structure that is usually built in this phase is an "inverted index".
#This is a dictionary that for every word (or for every query phrase) mantains a list of
#documents containing that word (query phrase) / advertisers requesting to appear on that word (query phrase).
#In this phase, we assume that there is a database in which we save for each document (advertiser, resp.)
#the link to the document (the name of the advertiser, resp.)d
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

pathPickles = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"
db_path = pathPickles+"db_Best_Match.txt"
limit = 20
#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
def create_word_advs():
    path = pathPickles
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

    file_word_advs = open(path + "word_advs.pickle", "ab+")
    pickle.dump(word_advs, file_word_advs)
    file_word_advs.close()

    file_word_in_docs = open(path + "word_in_docs.pickle", "ab+")
    pickle.dump(wordsInDoc, file_word_in_docs)
    file_word_in_docs.close()

    return [word_advs,wordsInDoc]


def best_match_opt(query, threshold,word_advs,sorted_word_advs,wordInDoc):

    cont_docs_analized=0
    adv_weights = dict()
    impact = list()
    query_words = query.split()

    residual_impact=0
    #Calcolo impatto di ogni parola della query
    for word in query_words:
        impact = insert_sorted(impact,word,((sorted_word_advs[word])[0])[1])

    global limit

    dict_20_docs = dict()
    list_word_scored = list()
    list_word_no_scored = list()
    count_docs = 0
    current_doc_index = 0

    for index_imp in range(len(impact)):
        word = impact[index_imp][0]
        residual_impact += impact[index_imp][1]
        if count_docs < limit:
            list_word_scored.append(word)
            current_doc_index = 0

            for doc in sorted_word_advs[word]:
                cont_docs_analized +=1
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
        adv_weights = score_doc(d, query_words, adv_weights, word_advs,wordInDoc)


    list_20_docs.clear()
    for doc in adv_weights:
        list_20_docs = insert_doc_1(doc,adv_weights[doc],list_20_docs)

    list_word_scored.remove(to_eliminate)
    #Punto 6,7

    counter = 1
    listaaaa = list(list_word_no_scored)

    contamio = 0
    for word in listaaaa:
        residual_impact -= sorted_word_advs[word][0][1]
        list_word_no_scored.remove(word)
        list_word_scored.append(word) # Aggiungo la nuova parola alla lista delle scored

        for i in range(current_doc_index,len(sorted_word_advs[word])):
            docss = (sorted_word_advs[word])[i] # Primo documento per cui bisogna fare lo score
            ds = docss[0]
            if (docss[0] not in adv_weights): # Docss potrebbe essere un canditato ad entrare nella lista
                freq_doc_no_scored = ((sorted_word_advs[word])[i])[1]
                # Punto 8
                cont_docs_analized +=1
                freq_doc_no_scored += residual_impact
                freq_doc_x = (list_20_docs[-1])[1]
                if freq_doc_no_scored > freq_doc_x: # Il 20esimo è meno pesante di quello che sta per entrare ?
                    len_list_20_doc = len(list_20_docs)
                    if len_list_20_doc == 20:
                        contamio+=1
                        doc20 = list_20_docs[len_list_20_doc-1]
                        adv_weights = score_doc(ds, query_words, adv_weights, word_advs, wordInDoc)
                        if (adv_weights[ds] > doc20[1]):
                            list_20_docs.remove(doc20)
                            docss[1] = adv_weights[docss[0]]
                            list_20_docs = insert_doc_1(docss[0],docss[1],list_20_docs)

                    else:
                        contamio+=1
                        adv_weights = score_doc(ds, query_words, adv_weights, word_advs,wordInDoc)
                        docss[1] = adv_weights[docss[0]]
                        list_20_docs = insert_doc_1(docss[0],docss[1],list_20_docs)

                else:
                    break

        current_doc_index = 0
        counter +=1
    return cont_docs_analized,list_20_docs



def score_doc (document,query_words, adv_weights, word_advs,wordInDoc):
    adv_weights[document] = 0
    for word in query_words:
        if document in word_advs[word]:
            if document in adv_weights:
                adv_weights[document] += (((word_advs[word])[document])[0])/wordInDoc[document]
    return adv_weights

def insert_sorted (impact, word, freq):
    l = list()
    l.append(word)
    l.append(freq)
    for i in range(len(impact)):
        if ((impact[i])[1] < freq):
            impact.insert(i,l)
            return impact
    impact.append(l)
    return impact


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

    size = len(l)

    if size == 20:
        if value < l[size-1][1]:
            return l
        else:
            l.pop(size - 1)

    lista_fons = list()
    lista_fons.append(key)
    lista_fons.append(value)
    for i in range(0,size-1):
        if ((l[i])[1] < value):

            l.insert(i,lista_fons)
            return l

    l.append(lista_fons)
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



