from Classic_Search.Best_Match.Best_match_optimization import *
import csv
import pickle

path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"

file_matching = open(path + "Matching_Dataset.pickle", "rb")
sorted_word_advs = pickle.load(file_matching)

query="facebook privacy security health video videos nba wired business google food games california tv team sport fons"
query_words = query.split(" ")

impact = list()

#Calcolo impatto di ogni parola della query
for word in query_words:
    impact = insert_sorted(impact,word,((sorted_word_advs[word])[0])[1])
print()

with open("/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/sorted_advs.csv", 'w') as csvfile:

    fieldnames = ['Word','sorted']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    # now data, assuming each column has the same # of values
    for word in query_words:
        writer.writerow({'Word': word, 'sorted': str(sorted_word_advs[word][0:1])})


    csvfile.close()