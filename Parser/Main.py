#Crea:
# out_file è il db che servirà a Best match
# Creazione del grafo per Page Rank

from Parser.Impl_Parser import *
from Classic_Search.PageRank.Graph import *
import os
import pickle


def getMostFamous (db,pathfile):
    w = dict()
    for doc in db:
        for word in db[doc]:
            if word in w:
                w[word] +=1
            else:
                w[word] = 1

    list_top_words = list()
    c=0
    for p in w:
        if c>=30:
            if (list_top_words[29])[1]<w[p]:
                list_top_words.pop()
                list_top_words = insert_s(p,w[p],list_top_words)
        else:
            list_top_words= insert_s(p,w[p],list_top_words)
            c+=1
    f=open(pathfile,"w")
    for i in range(len(list_top_words)):

        f.write(str(list_top_words[i][0])+"---"+str(list_top_words[i][1])+"\n")
    f.close()

def insert_s(key,value,l):
    lista_fons = list()
    lista_fons.append(key)
    lista_fons.append(value)
    for i in range(0,len(l)):
        if ((l[i])[1] < value):

            l.insert(i,lista_fons)
            return l

    l.append(lista_fons)
    return l

graph_path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/Ranking_Dataset.pickle"

db_path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/db_Best_Match.txt"

try:
    os.remove("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/db_Best_Match.txt")
except OSError:
    print ("File Già rimossi")
try:
    os.remove("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/Matching_Dataset.pickle")
except OSError:
    print("File Già rimossi")
try:
    os.remove("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/word_advs.pickle")
except OSError:
    print("File Già rimossi")
try:
    os.remove("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/word_in_docs.pickle")
except OSError:
    print("File Già rimossi")
try:
    os.remove("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/Complete_Graph_Dataset.pickle")
except OSError:
    print("File Già rimossi")
try:
    os.remove("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/Ranking_Dataset.pickle")
except OSError:
    print ("File Già rimossi")


out_file = open(db_path,"w")
file_parsed  = open(graph_path, "ab+")

path = os.getcwd()
print(path)
pathdataset = path+"/datasetRS"

graph_merge = list()

for i in os.listdir(pathdataset):
    if i.endswith(".pages"):
        path = pathdataset + "/" + i
        graph, db = read_wibbi(path)
        graph_merge.append(graph)

        getMostFamous(db,"/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/TopicSensitive/"+i[:-6]+".txt")

        for i in graph.keys():
            if (i == 'http://www.google.it/intl/it/earth/download/ge/'):
                print(i)
            if (len(db[i]) != 0):
                str = i +" "
                for line in db[i]:
                  str += line.lower()+","

                out_file.write(str[:-1]+"\n")

pickle.dump(graph_merge,file_parsed)
file_parsed.close()
out_file.close()


# Creazione del grafo
create_complete_graph("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/PageRank/",False)
