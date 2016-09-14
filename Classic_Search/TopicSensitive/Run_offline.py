import os
import pickle


def to_pickle():
    path_top_words = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/TopicSensitive/Top_Words/"
    pathPickles = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"

    diz = dict()
    for i in os.listdir(path_top_words):
        print(i)
        if i.endswith(".txt"):
            diz[i[:-4]] = dict()
            file = open(path_top_words+i,'r')
            for line in file:
                app=line.split("---")
                diz[i[:-4]][app[0]] = app[1]
        file.close()

    pickle_file = open(pathPickles+"Top_Words.pickle",'ab+')
    pickle.dump(diz,pickle_file)

    pickle_file.close()


#Creazione pickle di top words in Topic Sensitive
to_pickle()