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

#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
def create_word_advs():
    infile = open("database.txt")
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



def best_match_buono (query, threshold):
    adv_weights = dict()
    best_docs = set()
    array = create_word_advs()

    word_advs = array[0]
    wordsInDoc = array[1]

    query_words = query.split()

    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in word_advs[word]:


            if doc not in adv_weights.keys():
                adv_weights[doc] = (((word_advs[word])[doc])[0])/wordsInDoc[doc]
            else:
               adv_weights[doc] += (((word_advs[word])[doc])[0])/wordsInDoc[doc]
        #If we would like to count the occurrences, then we must increment the weights not by 1, but by the number of occurrence of that word in the document

        #We use a threshold to choose which document must be returned
            if adv_weights[doc] >= threshold:
                best_docs.add(doc)
    print(adv_weights)
    return best_docs

def best_match(query, threshold):
    adv_weights = dict()
    best_docs = set()
    array = create_word_advs()
    impact = list()
    word_advs = array[0]
    wordsInDoc = array[1]
    x = sort_docs(word_advs)

    query_words = query.split()

    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:

        impact = insert_sorted(impact,word,((x[word])[0])[1])
        for doc in word_advs[word]:
            if doc not in adv_weights.keys():
                adv_weights[doc] = ((word_advs[word])[doc])[0]
            else:
               adv_weights[doc] += ((word_advs[word])[doc])[0]
        #If we would like to count the occurrences, then we must increment the weights not by 1, but by the number of occurrence of that word in the document

        #We use a threshold to choose which document must be returned
            if adv_weights[doc] >= threshold:
                best_docs.add(doc)

    print (word_advs)
    print(x)
    print (impact)
    return best_docs

def insert_sorted (impact, word, freq):
    l = list()
    l.append(word)
    l.append(freq)
    for i in range(len(impact)):
        if ((impact[i])[1] < freq):
            impact.insert(i,l)
            return impact
    impact.append(l)
    return  impact





def calculate_frequency(word_advs, wordsInDoc):

    for word in word_advs:
        for doc in word_advs[word]:
            ((word_advs[word])[doc])[0] /= wordsInDoc[doc]
    return word_advs


def sort_docs (word_advs):

    sorted_w = dict()

    for word in word_advs:
        if word not in sorted_w:
            sorted_w[word] = list()
        for doc in word_advs[word]:
            sorted_w[word] = insert_sort_list(sorted_w[word],doc,((word_advs[word])[doc])[0])

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


#create_word_advs()
set = best_match("esempio prova",0)

#set2 = exact_match("prova esame")
#print(set)
#print(set2)
