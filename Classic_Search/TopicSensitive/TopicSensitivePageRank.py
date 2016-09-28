import pickle
from numpy import add,dot,multiply
from math import sqrt
from joblib import Parallel, delayed


def topicSensitiveVector(graph,categories_graph,best_categories):
    sensitive_vectors=dict() #rank
    nodes=graph.keys()
    size=0
    for i in range(len(best_categories)):
        cat = best_categories[i][0]
        size += len(categories_graph[cat])
    size=size*2
    for n in nodes: #per ogni nodo del grafo
        for cat in categories_graph: #per ogni categoria
            if n in categories_graph[cat]: #se il nodo in esame appartiene alla categoria in esame
                perc=is_cat_in_best_cat(cat, best_categories)
                if perc != 0: #se la categoria in esame è tra le best
                    o = (1/size)
                    u = (perc*0.0000025)
                    sensitive_vectors[n] = o+u #ok rankalo
                    break
                else:
                    sensitive_vectors[n] = 0

    return sensitive_vectors

#
# Return a list of best categories ordered by appearing times in each query term
def getBestCat(query, pickwords,word_X_cat):
    word_categories_weight = dict()
    query_split = query.split(" ")
    for i in query_split:
        set_of_categories = word_X_cat[i] #whereis(i, pickwords)
        word_categories_weight[i] = list()
        #for list_cat in word_X_cat:
        for el in set_of_categories:
            word_categories_weight[i].append(el)
            # per ogni parola word_categories_weight mantiene la lista delle categorie in cui compare e con quale peso

            # prendere le migliori categorie
    best_cat = dict()
    for word in word_categories_weight:
        for cat in word_categories_weight[word]:
            #peso = word_categories_weight[word][index_cat][1]
            if cat in best_cat:
                best_cat[cat] += 1
            else:
                best_cat[cat] = 1

    toReturn = list()
    for cat in best_cat:
        toReturn = insert_sorted_to_list(cat,best_cat[cat],toReturn)

    return toReturn


def insert_sorted_to_list(key,value,l):
    lista_fons = list()
    lista_fons.append(key)
    lista_fons.append(value)
    for i in range(0,len(l)):
        if ((l[i])[1] < value):

            l.insert(i,lista_fons)
            return l

    l.append(lista_fons)
    return l


#pw = dizionario <categoria,parola>
def whereis(term,pw):
    categoria=list()
    app = list()
    for k in pw:
        if term in pw[k]:
            categoria.append(k)
            #app.append(k)
            #app.append(pw[k][term]) #peso
            #categoria.append(app) # categoria e peso del termine

    return categoria

def topicSensitiveRanking(graph,s,step,confidence,query,categories_graph,pickwords,word_cat):
    done = 0
    time = 0

    # Initialization
    best_categories=getBestCat(query,pickwords,word_cat)
    best_categories=calculate_percentage(best_categories)

    rank=topicSensitiveVector(graph,categories_graph,best_categories)

    listaraf = list(reversed(sorted(rank.items(), key=lambda x: x[1])))[:40]

    print(listaraf)
    sum = 0
    for r in rank:
        sum +=rank[r]

    tmp = dict()
    nodes = graph.keys()
    n = len(nodes)
    while not done and time < step:
        time += 1


        for i in nodes:
            if (isIn(i,best_categories,categories_graph)):
                tmp[i] = float(1 - s) / (len(best_categories)*2000)# Each nodes receives a share of 1/n with probability 1-s
            else:
                tmp[i] = 0 # non riceve niente

        for i in nodes:
            #if (isIn(i, best_categories, categories_graph)):
            for j in graph[i]:
                tmp[j] += float(s * rank[i]) / len(graph[i])  # Each nodes receives a fraction of its neighbor rank with probability s

        # Computes the distance between the old rank vector and the new rank vector in L_1 norm
        diff = 0
        for i in nodes:
            diff += abs(rank[i] - tmp[i])
            rank[i] = tmp[i]

        if diff <= confidence:
            done = 1

    return time, rank, best_categories


def calculate_percentage(best_cat):
    tot = 0
    for cat in range(len(best_cat)):
        tot += best_cat[cat][1]


    for cat in range(len(best_cat)):
        percentage=(100/tot)*best_cat[cat][1]
        best_cat[cat][1] = percentage

    return best_cat



def isIn(doc,best_cat,cat_graph):
    for index_cat in range(len(best_cat)):
        cat = best_cat[index_cat][0]
        if doc in cat_graph[cat]:
            return True
    return False


def is_cat_in_best_cat(cat,best_categories):
    for i in range(len(best_categories)):
        if cat == best_categories[i][0]:
            return best_categories[i][1]
    return 0


def execute(sgraph, sdegree, srank, s):
    nodes = sgraph.keys()

    tmp = dict()

    for i in nodes:
        for j in sgraph[i]:
            if j not in tmp:
                tmp[j] = 0
            tmp[j] += float(s * srank[i]) / sdegree[i]

    return tmp


# This function implements the operation of combining the components computed by 'execute'
# and compute the new rank.
# In particular, it takes in input vectors computed by 'execute' on input block[i][j] for every i
# and sums the contributions of these vectors.
# It also adds to each element the contribution of teleportation.
# In this way, we achieve the new page rank for all nodes in the j-th block.
# Note that the function needs to save in memory
# k + 2 vectors of n/k elements:
#    one for the list of nodes in the j-th block
#    one for the new rank values of these nodes
#    k vectors to combine
def combine(nodes, vectors, s, n,best_categories,cat_graph):
    tmp = dict()

    for j in nodes:
        if isIn(j,best_categories,cat_graph):
            tmp[j] = float(1 - s) / (len(best_categories)*2000)
        else:
            tmp[j] = 0
            for i in range(len(vectors)):
                if j in vectors[i]:
                    tmp[j] += vectors[i][j]

    return tmp


# This function implements the operation of computing the difference between the new and the old rank vector.
def verify(rank, tmp):
    diff = 0

    for i in rank.keys():
        diff += abs(rank[i] - tmp[i])

    return diff

def topic_sensitive_parallel(graph,graph2, degree, n, s, step, confidence, num_jobs,categories_graph,pickwords,word_cat,query):

    best_categories = getBestCat(query, pickwords, word_cat)
    best_categories = calculate_percentage(best_categories)
    done = 0
    time = 0
    k = int(sqrt(num_jobs))

    # Each info about the nodes of graph is represented as a vector of k blocks.
    # Block[i] contains the info of nodes in the i-th subset.

    rank_sens=topicSensitiveVector(graph2,categories_graph,best_categories)
    listaraf = list(reversed(sorted(rank_sens.items(), key=lambda x: x[1])))[:40]

    print(listaraf)

    # Info: rank
    rank = []
    for i in range(k):
        rank.append(dict())
        for j in degree[i].keys():
            #if (isIn(j,best_categories,categories_graph)):
            rank[i][j] = rank_sens[j]#float(1) / (len(best_categories)*2000)


            #rank[i][j] = float(1) / n  # Initial value

    # Info: temporary rank
    tmp = []
    for i in range(k):
        tmp.append(dict())

    # Next instruction create a set of num_jobs processes and names this set parallel.
    # If you prefer to create threads in place of processes, you must write Parallel(n_jobs=num_jobs,backend="threading")
    with Parallel(n_jobs=num_jobs) as parallel:

        while not done and time < step:
            time += 1

            # Next instruction asks to the set of processes created above to run the function execute with the given parameters.
            # Note that they correspond to k^2 = num_jobs runs, one for each process.
            # It is possible to assign less or more runs than the number of processes.
            # In these cases there will processes that do nothing or others that do more job than others.
            # The output of each execution is saved in a vector:
            # the i-th entry of this vector contains the output of the i-th execution.
            # In our case, result[0] contains the output of execute when j=0 and i=0,
            # result[1] contains the output of execute when j=0 and i=1,
            # result[k] contains the output of execute when j=1 and i=0, and so on.
            results = parallel(delayed(execute)(graph[i][j], degree[i], rank[i], s) for j in range(k) for i in range(k))

            # Next instruction asks to the set of processes created above to run the function combine with the given parameters.
            tmp = parallel(delayed(combine)(list(degree[j].keys()), results[j * k:(j + 1) * k], s, n,best_categories,categories_graph) for j in range(k))

            diff = 0

            # Next instruction asks to the set of processes created above to run the function verify with the given parameters.
            differences = parallel(delayed(verify)(rank[i], tmp[i]) for i in range(k))

            for i in range(k):
                diff += differences[i]
                rank[i] = tmp[i].copy()

            if diff <= confidence:
                done = 1

    return time, rank
