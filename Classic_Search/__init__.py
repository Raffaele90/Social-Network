import csv
import pickle





path = "/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search/Pickles/"

file_matching = open(path + "Matching_Dataset.pickle", "rb")
sorted_word_advs = pickle.load(file_matching)

with open('/Users/raffaeleschiavone/PycharmProjects/Social-Network/Classic_Search_categorie.csv', 'w') as csvfile:
    diz = dict()
    query="facebook health video"
    for q in query.split(" "):
        if q not in diz:
            diz[q] = list()
        l = sorted_word_advs[q]
        for i in l:
            diz[q].append(i)

    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(list(diz.keys()))
    # now data, assuming each column has the same # of values
    for i in range(20):
        csvWriter.writerow([diz[k][i] for k in diz.keys()])

    diz = dict()
    query = "nba sport"
    for q in query.split(" "):
        if q not in diz:
            diz[q] = list()
        l = sorted_word_advs[q]
        for i in l:
            diz[q].append(i)

    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(list(diz.keys()))
    # now data, assuming each column has the same # of values
    for i in range(20):
        csvWriter.writerow([diz[k][i] for k in diz.keys()])

#    writer = csv.writer(csvfile)
#   for key, value in diz.items():
#        writer.writerow([key, value])



    csvfile.close()