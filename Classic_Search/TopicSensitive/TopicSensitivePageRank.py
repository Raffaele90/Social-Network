import pickle
def topicSensitiveVector(graph,categories_graph,best_categories):
    sensitive_vectors=dict() #rank
    nodes=graph.keys()
    size=0
    for i in best_categories:
        size += len(categories_graph[i])
    for n in nodes: #per ogni nodo del grafo
        for cat in categories_graph: #per ogni categoria
            if n in categories_graph[cat]: #se il nodo in esame appartiene alla categoria in esame
                if cat in best_categories: #se la categoria in esame è tra le best
                    sensitive_vectors[n] = 1/size #ok rankalo --> combinazione lineare a*v1 + b*v2 +...+ j*vi +...
                    break
                else:
                    sensitive_vectors[n] = 0

    return sensitive_vectors

def getBestCat(query,pickwords):
    word_categories_weight=dict()
    for i in query:
        word_categories_weight[i]=whereis(query[i],pickwords)
        #per ogni parola word_categories_weight mantiene la lista delle categorie in cui compare e con quale peso

    #prendere le migliori categorie


    return list_best_cat

def whereis(term,pw):
    categoria=list()
    for k in pw:
        if term in pw[k]:
            app=list()
            app.append(k)
            app.append(pw[k][term]) #peso
        categoria.append(app) # categoria e peso del termine
    return categoria

def topicSensitiveRanking(graph,s,step,confidence,query,categories_graph,pickwords):
    done = 0
    time = 0

    # Initialization
    rank = dict()
    #categories_graph=pickle.load("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/Categories_Graph.pickle")
    #pick_words = pickle.load("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/Categories_Graph.pickle")
    best_categories=getBestCat(query,pickwords)
    rank=topicSensitiveRanking(graph,categories_graph,best_categories)

    tmp = dict()
    while not done and time < step:
        time += 1

        for i in nodes:
            tmp[i] = float(1 - s) / n  # Each nodes receives a share of 1/n with probability 1-s

        for i in nodes:
            for j in graph[i]:
                tmp[j] += float(s * rank[i]) / len(
                    graph[i])  # Each nodes receives a fraction of its neighbor rank with probability s

        # Computes the distance between the old rank vector and the new rank vector in L_1 norm
        diff = 0
        for i in nodes:
            diff += abs(rank[i] - tmp[i])
            rank[i] = tmp[i]

        if diff <= confidence:
            done = 1

    return time, rank