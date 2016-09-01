from Classic_Search.PageRank.PageRank import *
import pickle
import timeit


from numpy import add,dot,multiply
from math import sqrt
from joblib import Parallel, delayed


def create_struct_parallel(graph,k):

    subsets = list()
    subsets = split_g(graph,k)
    graph_splitted=crea_mat(k)
    graph_splitted=scatter(graph_splitted,graph,subsets)

    '''if 'http://europa.eu/pol/emu/index_it.htm' in graph_splitted[0][0]:
        x=graph_splitted[0][0]['http://europa.eu/pol/emu/index_it.htm']

    if 'http://europa.eu/pol/emu/index_it.htm' in graph_splitted[0][1]:
        z=graph_splitted[0][1]['http://europa.eu/pol/emu/index_it.htm']
    if 'http://europa.eu/epso/index_it.htm'in graph_splitted[1][0]:
        q=graph_splitted[1][0]['http://europa.eu/epso/index_it.htm']
    if 'http://europa.eu/epso/index_it.htm' in graph_splitted[1][1]:
        u=graph_splitted[1][1]['http://europa.eu/epso/index_it.htm']
'''
    degrees=getdeg(graph,k,subsets)


    print()


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

'''

path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/Complete_Graph_Dataset.pickle"
file_graph = open(path, "rb")
graph = pickle.load(file_graph)



# Graph is represented with its adjacency lists
simple = dict()
simple['x'] = {'y','z','w'}
simple['y'] = {'x','w'}
simple['z'] = {'x'}
simple['w'] = {'y','z'}

degree,simple=create_struct_parallel(simple,2)


start_time = timeit.default_timer()
time, rank = pageRank3(simple, degree, 4, 0.85, 60, 0, 4)
elapsed = timeit.default_timer() - start_time

print (rank[0:20])
print(elapsed)


# Graph is represented with its adjacency lists
simple = dict()
simple['x'] = {'y','z','w'}
simple['y'] = {'x','w'}
simple['z'] = {'x'}
simple['w'] = {'y','z'}

start_time = timeit.default_timer()
time2, rank2 = pageRank2(simple,0.85,60,0)
elapsed2 = timeit.default_timer() - start_time

print(rank2, time2, elapsed2)

'''