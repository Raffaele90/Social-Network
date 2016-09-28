from Classic_Search.PageRank.PageRank import *
import pickle
import timeit


from numpy import add,dot,multiply
from math import sqrt
from joblib import Parallel, delayed


def create_struct_parallel(graph,k):

    subsets = split_g(graph,k)
    graph_splitted=crea_mat(k)
    graph_splitted=scatter(graph_splitted,graph,subsets)
    degrees=getdeg(graph,k,subsets)


    return [degrees,graph_splitted]


def split_g(graph,k):
    l = list()
    soglia = len(graph)/k
    listarella=toList(graph)
    start=0
    for j in range(k):
        l.append(dict())
        counter=0
        for i in range(start,len(listarella)):
            if counter < soglia:
                l[j][listarella[i]] = graph[listarella[i]]
                counter+=1
            else:
                start=i
                break
    return l


def toList(g):
    lista=list()
    for key in g.keys():
        lista.append(key)
    return lista


def crea_mat(k):
    mat=list()
    for i in range(k):
        mat.append([])
        for j in range(k):
            mat[i].append(dict())
    return mat


def scatter1(gsplit,g,subsets):
    size=len(gsplit)
    for i in range(size):
        for key in subsets[i]:
            for j in range(size):
                app=g[key]
                gsplit[i][j][key]=set.intersection(app,subsets[j])

    return gsplit

def scatter(gsplit,g,subsets):
    size=len(gsplit)
    for i in range(size):
        for j in range(size):
            for key in subsets[i]:
                app = g[key]
                gsplit[i][j][key] = set.intersection(app,subsets[j])
    return gsplit



def getdeg(g,k,subsets):
    deg=[]
    for i in range(k):
        deg.append(dict())
    for j in range(len(subsets)):
        for k in subsets[j]:
            deg[j][k]=len(g[k])
    return deg

