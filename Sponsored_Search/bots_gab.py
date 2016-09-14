#!/usr/bin/python

import random


def computeHarm(slot_ctrs, sort_slots, adv_bids, current_slot, current_adv):
    sw_no_curr_adv = 0
    no_adv_bids = adv_bids.copy()
    del no_adv_bids[current_adv]
    sort_no_adv_bids = sorted(no_adv_bids.values(), reverse=True)

    for i in range(min(len(sort_slots), len(sort_no_adv_bids))):
        sw_no_curr_adv += slot_ctrs[sort_slots[i]] * sort_no_adv_bids[i]

    sw_noadv_noslot = 0
    no_currslot = sort_slots[:]
    del no_currslot[current_slot]

    for i in range(min(len(no_currslot), len(sort_no_adv_bids))):
        sw_noadv_noslot += slot_ctrs[no_currslot[i]] * sort_no_adv_bids[i]

    return sw_no_curr_adv - sw_noadv_noslot


#The bot of an advertiser is a program that, given the history of what occurred in previous auctions, suggest a bid for the next auction.
#Specifically, a bot takes in input
#- the name of the advertiser (it allows to use the same bot for multiple advertisers)
#- the value of the advertiser (it is necessary for evaluating the utility of the advertiser)
#- the clickthrough rates of the slots
#- the history
#We assume the history is represented as an array that contains an entry for each time step,
#i.e. history[i] contains the information about the i-th auction.
#In particular, for each time step we have that 
#- history[i]["adv_bids"] returns the advertisers' bids as a dictionary in which the keys are advertisers' names and values are their bids
#- history[i]["adv_slots"] returns the assignment as a dictionary in which the keys are advertisers' names and values are their assigned slots
#- history[i]["adv_pays"] returns the payments as a dictionary in which the keys are advertisers' names and values are their assigned prices

#The bot that we implement here is a symple best_response bot:
#it completely disregards the history except the last step,
#and suggest the bid that will maximize the advertiser utility
#given that the other advertisers do not change their bids.
def best_response(name, adv_value, slot_ctrs, history, auction, budget):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        if auction == "fp":
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
        else:
            tmp_pay = computeHarm(slot_ctrs, sort_slots, adv_bids, i, name)
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    if preferred_slot == -1:
        # TIE-BREAKING RULE: I choose the largest bid smaller than my value for which I lose
        return min(adv_value, sort_bids[len(sort_slots)])
    
    if preferred_slot == 0:
        # TIE-BREAKING RULE: I choose the bid that is exactly in the middle between my own value and the next bid
        return float(adv_value+payment)/2
    
    #TIE-BREAKING RULE: If I like slot j, I choose the bid b_i for which I am indifferent from taking j at computed price or taking j-1 at price b_i
    return (adv_value - float(slot_ctrs[sort_slots[preferred_slot]])/slot_ctrs[sort_slots[preferred_slot-1]] * (adv_value - payment))
    
#submits the highest possible bid that gives the desired slot
def best_response_competitive(name, adv_value, slot_ctrs, history, auction, budget):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        if auction == "fp":
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
        else:
            tmp_pay = computeHarm(slot_ctrs, sort_slots, adv_bids, i, name)  
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
   
    if preferred_slot == -1:
        return min(adv_value, sort_bids[len(sort_slots)])
    
    if preferred_slot == 0:
        return float(adv_value)
    
    return min(adv_value, float(sort_bids[preferred_slot-1] - 1))

#submits the lowest possible bid that gives the desired slot
def best_response_altruistic(name, adv_value, slot_ctrs, history, auction, budget):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)
    sort_slots=sorted(slot_ctrs.keys(), key=slot_ctrs.__getitem__, reverse=True)
    
    #Saving the index of slots assigned at the advertiser in the previous auction
    if name not in adv_slots.keys():
        last_slot=-1
    else:
        last_slot=sort_slots.index(adv_slots[name])
        
    utility = -1
    preferred_slot = -1
    payment = 0

    #The best response bot makes the following steps:
    #1) Evaluate for each slot, how much the advertiser would pay if
    #   - he changes his bid so that that slot is assigned to him
    #   - no other advertiser change the bid
    for i in range(len(sort_slots)):
        if auction == "fp":
            tmp_pay = sort_bids[i] #then, I must pay for that slot the bid of the advertiser at which that slot was previously assigned
        else:
            tmp_pay = computeHarm(slot_ctrs, sort_slots, adv_bids, i, name)
    #2) Evaluate for each slot, which one gives to the advertiser the largest utility
        new_utility = slot_ctrs[sort_slots[i]]*(adv_value-tmp_pay)
        
        if new_utility > utility:
            utility = new_utility
            preferred_slot = i
            payment = tmp_pay
    
    #3) Evaluate which bid to choose among the ones that allows the advertiser to being assigned the slot selected at the previous step
    if preferred_slot == -1:
        return min(adv_value, sort_bids[len(sort_slots)])
    return min(adv_value, float(payment + 1))


#always submits a bid greater than the highest bid seen in previous auction, even if it is greater than own value
def competitor_bursting(name, adv_value, slot_ctrs, history, auction, budget):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return adv_value
    
    #Initialization
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values(), reverse=True)

    return sort_bids[0] + random.random()
        
#always submits that is the minimum among the last non-winning bid and the advertiser value for the query
def budget_saving(name, adv_value, slot_ctrs, history, auction, budget):
    
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return random.randrange(0, adv_value)
    
    #Initialization
    adv_slots=history[step-1]["adv_slots"]
    adv_bids=history[step-1]["adv_bids"]
    
    adv_no_winners = adv_bids.copy()
    for name in adv_slots.keys():
        del adv_no_winners[name]
    
    sort_bids=sorted(adv_no_winners.values())
    
    if len(sort_bids) == 0:
        return random.randrange(0, adv_value)
    return min(adv_value, sort_bids[0])


def bot_random(name, adv_value, slot_ctrs, history, auction, budget):
        
    step = len(history)

    # If this is the first step there is no history and no best-response is possible
    # We suppose that adevertisers simply bid their value.
    # Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.

    if step==0 or adv_value == 0:
        return 0


    
    #Initialization
    adv_bids=history[step-1]["adv_bids"]
    
    sort_bids=sorted(adv_bids.values())
    
    return random.randrange(0, adv_value)
    
#do competitor-bursting as long as your current budget is half the initial budget and then do best-response or do competitor bursting for queries for which the advertiser value is high and budget-saving for the others
def combination(name, adv_value, slot_ctrs, adv_sbudgets, adv_cbudgets, history, auction, threshold):
        
    step = len(history)
    
    #If this is the first step there is no history and no best-response is possible
    #We suppose that adevertisers simply bid their value.
    #Other possibilities would be to bid 0 or to choose a bid randomly between 0 and their value.
    if step == 0:
        return 0
    br = None
    if adv_cbudgets >= adv_sbudgets/2:
        br = competitor_bursting(name, adv_value, slot_ctrs, history)
    else:         
        if adv_value > threshold:
            br = best_response(name, adv_value, slot_ctrs, history)
        else:
            br = budget_saving(name, adv_value, slot_ctrs, history)
    return br
