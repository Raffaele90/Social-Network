import time
import pickle
import os
from Classic_Search.Best_Match.Best_match_optimization import *

def calcolo_top_parole():
    path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Best_Match/"
    file_matching = open(path + "Matching_Dataset.pickle", "rb")
    sorted_word_advs = pickle.load(file_matching)
    file_matching.close()
    impact = list()
    print ("Parole in sorted advs"+ str(len(sorted_word_advs)))
    for word in sorted_word_advs:
        impact = insert_sorted(impact, word, ((sorted_word_advs[word])[0])[1])

    print(impact[0])
    print(impact[1])
    print(impact[2])





calcolo_top_parole()