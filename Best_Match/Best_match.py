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

#We create an inverted index with an entry for every query search on which advertisers requested to appear
def create_query_advs():
    
    infile = open("database.txt")
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

    return [word_advs,wordsInDoc]



def best_match(query, threshold):
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



#create_word_advs()
set = best_match("esempio prova",0)
print(set)

#set2 = exact_match("prova esame")
#print(set)
#print(set2)
