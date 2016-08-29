import time
import pickle
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

###EXACT MATCH###


db_path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/db_Best_Match.txt"


#We create an inverted index with an entry for every query search on which advertisers requested to appear
def create_query_advs():
    
    infile = open(db_path)
    query_advs = dict()
    
    for line in infile:
        name_list = line.split(' ',1) #It splits the line in two elements: the first contains the name of the advertiser, the second a list of query searches
        name=name_list[0]
        queries=name_list[1].split(',') #It splits the list query searches
        
        for query in queries:
            
            query_key = ' '.join(sorted(query.split())) #We reoder every query search so that "prova esame" is the same as "esame prova"
            
            if query_key not in query_advs.keys():
                query_advs[query_key]=[]
                
            query_advs[query_key].append(name)
    return query_advs


#To return an exact match we have to simply return the list that corresponds to the given query in the inverted index    
def exact_match(query):
    query_advs = create_query_advs()
    ' '.join(sorted(query.split())) #We reorder the query in the lexicographic order
    
    return query_advs[query]

###BEST MATCH###

#We create an inverted index with an entry for every word of a document or for any word on which advertisers requested to appear
def create_word_advs():
    path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/"

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

    file_word_advs = open(path + "word_advs.pickle", "ab+")
    pickle.dump(word_advs, file_word_advs)
    file_word_advs.close()

    file_word_in_docs = open(path + "word_in_docs.pickle", "ab+")
    pickle.dump(wordsInDoc, file_word_in_docs)
    file_word_in_docs.close()

    return [word_advs,wordsInDoc]



def best_match(query, threshold):
    adv_weights = dict()
    path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/"
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

    query_words = query.split()

    #For every word we look at each document in the list and we increment the document's weight
    for word in query_words:
        for doc in word_advs[word]:


            if doc not in adv_weights.keys():
                adv_weights[doc] = (((word_advs[word])[doc])[0])/wordsInDoc[doc]
            else:
               adv_weights[doc] += (((word_advs[word])[doc])[0])/wordsInDoc[doc]
        #If we would like to count the occurrences, then we must increment the weights not by 1, but by the number of occurrence of that word in the document



    list_20_docs = list()
    for doc in adv_weights:
        if adv_weights[doc] >= threshold:
            list_20_docs = insert_doc_1(doc,adv_weights[doc],list_20_docs)

    #print(adv_weights)
    '''for d in best_docs:
        print(d)
        print(adv_weights[d])'''


    return list_20_docs[0:19]


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
#start_time = time.time()

#set = best_match("Facebook Twitter information",0)
#print("--- %s seconds ---" % (time.time() - start_time))
#print(set)

#set2 = exact_match("prova esame")
#print(set)
#print(set2)
