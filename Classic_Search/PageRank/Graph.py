#!/usr/bin/python

import random
import pickle
import os


# Lo script sceglie 10 vertici randomici tra coppie di set di 2000 pagine
# con u appartenente al primo set e v appartenente al secondo set ed
# aggiunge un link tra u e v se questo link non esiste già

# creazione del grafo connesso completo
# sarà utilizzato per gli algoritmi di ranking

def create_complete_graph(pathdataset,verbose):
    file_parsing = open(pathdataset + "Ranking_Dataset.pickle", "rb")
    graph_merge = pickle.load(file_parsing)

    for k in range(0, len(graph_merge) - 1):
        for i in range(k+1, len(graph_merge)):
            list_u = random.sample(list(graph_merge[k].keys()), 10)
            list_v = random.sample(list(graph_merge[i].keys()), 10)
            for j in range(10):
                if (verbose):
                    print("Prima: ", graph_merge[k])
                for z in range(10):
                    if not (list_u[j] in graph_merge[i][list_v[z]]):
                        graph_merge[i][list_v[z]].add(list_u[j])
                    if not (list_v[j] in graph_merge[k][list_u[z]]):
                        graph_merge[k][list_u[z]].add(list_v[j])
                if (verbose):
                    print("Dopo: ", graph_merge[k])

    file_connection = open(pathdataset + "Complete_Graph_Dataset.pickle", "ab+")
    complete_graph = dict()

    for cat in graph_merge:
        complete_graph.update(cat)

    pickle.dump(complete_graph, file_connection)
    file_connection.close()

def prova_graph(g):

    for k in range(0, len(g) - 1):
        for i in range(k+1, len(g)):
            list_u = random.sample(list(g[k].keys()), 2)
            list_v = random.sample(list(g[i].keys()), 2)
            for j in range(2):
                for z in range(2):
                    if not (list_u[j] in g[i][list_v[z]]):
                        g[i][list_v[z]].add(list_u[j])
                    if not (list_v[j] in g[k][list_u[z]]):
                        g[k][list_u[z]].add(list_v[j])

    print(g)

    #file_connection = open(pathdataset + "Complete_Graph_Dataset.pickle", "ab+")
    complete_graph = dict()

    for cat in g:
        complete_graph.update(cat)

    #pickle.dump(complete_graph, file_connection)
    #file_connection.close()

#path = os.getcwd()
#pathdataset = path + "/datasetRS/pickle/"
'''lg=list()
app1=dict()
app2=dict()
app1['A']=set()
app1['A'].add('C')
app1['A'].add('E')
app1['B']=set()
app1['B'].add('F')
app1['B'].add('A')
app1['B'].add('C')
app2['C']=set()
app2['C'].add('D')
app2['D']=set()
app2['D'].add('F')
app2['E']=set()
lg.append(app1)
lg.append(app2)'''
#create_complete_graph("../Parser/",False)
#prova_graph(lg)



