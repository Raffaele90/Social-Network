#!/usr/bin/python

import numpy

from random import randint, random
from Sponsored_Search.bots_gab import *
from Sponsored_Search.balance import *

def generate_random_configuration(queries, slots, advs):

    #Slots' clickthrough rates
    slot_ctrs = dict()
    for query in queries:
        slot_ctrs[query] = dict()
        for slot in slots:
            slot_ctrs[query][slot] = random.random()

    #Advertisers' budgets
    adv_budgets=dict()
    for adv in advs:
        adv_budgets[adv] = random.randrange(10, 1000)+1

    #Advertisers' values
    adv_values = dict()
    for adv in advs:
        adv_values[adv] = dict()
        for query in queries:
            adv_values[adv][query] = random.randrange(0, 30)

    return slot_ctrs, adv_budgets, adv_values

def set_bot(advs, bot_function):
    #Advertisers' bots
    adv_bots=dict()
    for adv in advs:
        adv_bots[adv] = bot_function

    return adv_bots


# Generate a random sequence of num_query queries, with each query selected from the list queries
def create_random_query_sequence(num_query, queries):
    query_sequence = []
    for i in range(num_query):
        query_sequence.append(queries[randint(0, len(queries) - 1)])
    return query_sequence


def create_history(possibile_queries):
    history = dict()
    for query in possibile_queries:
        history[query] = []
    return history

def run_auction(slot_ctrs, adv_sbudgets, adv_values, adv_bots, query, auction, bot_function , history):

    adv_cbudgets=adv_sbudgets.copy() #The current budgets of advertisers

    step=0
    adv_bids=dict()
    adv_bids[query] = dict()

    done=False
    max_step=100
    query_winners = 0
    adv_pays = 0

    for i in adv_values.keys():
        #Invoke the bots for computing the bids for each advertiser
         adv_bids[query][i] = adv_bots[i](i,adv_values[i][query],slot_ctrs[query],history[query],auction,adv_cbudgets[i])


    #Execute the auction with the bids computed above
    if auction == "fp":
        query_winners, adv_pays = balance(slot_ctrs, adv_bids, adv_sbudgets, adv_cbudgets, query)
    if auction == "vcg":
        query_winners, adv_pays = balanceVCG(slot_ctrs, adv_bids, adv_sbudgets, adv_cbudgets, query)
    adv_slots = dict()
    for slot in query_winners:
        adv_slots[query_winners[slot]] = slot
    #Update the history
    history[query].append(dict())
    history[query][len(history[query])-1]["adv_bids"]=dict(adv_bids[query])
    history[query][len(history[query])-1]["adv_slots"]=dict(adv_slots)
    history[query][len(history[query])-1]["adv_pays"]=dict(adv_pays)

    return query_winners, adv_pays

def calculate_utility(utility):
    sum = 0
    num_elem = 0
    for adv in utility.keys():
        for query in utility[adv]:
            sum += numpy.sum(utility[adv][query])
            num_elem += len(utility[adv][query])
    avg = sum / float(num_elem)
    return avg

def create_utility(advs, query_sequence):
    utility = dict()
    for adv in advs:
        utility[adv] = dict()
        for query in query_sequence:
            utility[adv][query] = []
    return utility


#All possible queries
queries=["prova","test","esempio","tanto il contenuto della query non cambia nulla"]
num_random_configuration = 500
num_query = 50
slots = ["id1", "id2", "id3"]
advs = ["x", "y", "z"]
auctions = ["fp", "vcg"]
adv_bots = [ best_response, best_response_competitive, best_response_altruistic]
query_sequence = create_random_query_sequence(num_query, queries)

utility = dict()
for adv in advs:
    utility[adv] = dict()
    for query in query_sequence:
        utility[adv][query] = []
for i in range(num_random_configuration):
    slot_ctrs, adv_sbudgets, adv_values = generate_random_configuration(query_sequence, slots, advs)
    print("slot_ctrs ", slot_ctrs, " adv_sbudgets ", adv_sbudgets, "adv_values ", adv_values)
    for auction in auctions:
        for adv_bot in adv_bots:
            revenue = 0
            adv_cbudgets = adv_sbudgets.copy()
            history = create_history(queries)
            utility = create_utility(advs, query_sequence)
            for query in query_sequence:
               # print("QUERY: ",query)
                query_winners, query_pay = run_auction(slot_ctrs, adv_cbudgets, adv_values, set_bot(advs,adv_bot), query, auction, adv_bot ,history)
                for j in query_winners.keys():
                    # We now simulate an user clicking on the ad with a probability that is equivalent to the slot's clickthrough rate
                    p = random.random()  # A number chosen uniformly at random between 0 and 1
                    if p < slot_ctrs[query][j]:  # This event occurrs with probability that is exactly slot_ctrs[query_sequence[i]][j]
                        adv_cbudgets[query_winners[j]] -= query_pay[query_winners[j]]
                        revenue += query_pay[query_winners[j]]
                        utility[query_winners[j]][query].append(adv_values[query_winners[j]][query] - query_pay[query_winners[j]])

                #print(query_winners, query_pay, adv_cbudgets)

            print("Auction:",auction,"\tBot:",adv_bot)
            print("\tAuctioneer revenue: ",revenue)
            print("\tAverage utility: ",calculate_utility(utility))
