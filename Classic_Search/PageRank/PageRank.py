#!/usr/bin/python

from numpy import add,dot,multiply
from math import sqrt
from joblib import Parallel, delayed

import pickle


def pageRank1(graph, s, step, confidence):
  n = len(graph)
  nodes = range(n)
  done = 0
  time = 0
  
  #Initialization
  rank = []
  tax = []
  for i in nodes:
    rank.append(float(1)/n) #Initial rank vector
    tax.append(float(1-s)/n) #Tax vector
    
  while not done and time < step:
    time += 1
    
    #Execution of the PageRank iteration sMv + (1-s)t, where
    #s is the taxation parameter in input
    #M the adhacency list of the graph,
    #v the actual rank vector
    #t is the taxation vector
    tmp = add(dot(multiply(s,graph),rank),tax)
    
    #Computes the distance between the old rank vector and the new rank vector in L_1 norm
    diff = 0
    for i in nodes:
      diff += abs(rank[i]-tmp[i])
      rank[i] = tmp[i]
    
    if diff <= confidence:
      done = 1
    
  return time, rank

def pageRank2(graph,s,step,confidence):
  nodes=graph.keys()
  n=len(nodes)
  done = 0
  time = 0
  
  #Initialization
  rank = dict()
  for i in nodes:
    rank[i]=float(1)/n 
  
  tmp=dict()
  while not done and time < step:
    time += 1
    
    for i in nodes:
      tmp[i] = float(1-s)/n #Each nodes receives a share of 1/n with probability 1-s
    
    for i in nodes:
      for j in graph[i]:
        tmp[j] += float(s*rank[i])/len(graph[i]) #Each nodes receives a fraction of its neighbor rank with probability s 
    
    #Computes the distance between the old rank vector and the new rank vector in L_1 norm
    diff = 0
    for i in nodes:
      diff += abs(rank[i]-tmp[i])
      rank[i] = tmp[i]
    
    if diff <= confidence:
      done = 1
    
  return time, rank

#This function implements the operation executed by a single process.
#It consists of computing the product of block[i][j] with rank[i].
#Note that it only need to save in memory
#- n/k adjacency lists, each one with at most n/k elements
#- 3 vectors of n/k elements:
#    one for the degrees, 
#    one for the previous ranks, 
#    one for the values computed by this function
#Hence, if k is sufficiently large all these information
#can be stored in the processor memory.
#Thus we avoid the necessity of swapping from a faster memory to a slower memory
def execute(sgraph,sdegree,srank,s):
    nodes=sgraph.keys()
    
    tmp=dict()
    
    for i in nodes:
        for j in sgraph[i]:
            if j not in tmp:
                tmp[j]=0
            tmp[j] += float(s*srank[i])/sdegree[i]
            
    return tmp

#This function implements the operation of combining the components computed by 'execute'
#and compute the new rank.
#In particular, it takes in input vectors computed by 'execute' on input block[i][j] for every i
#and sums the contributions of these vectors.
#It also adds to each element the contribution of teleportation.
#In this way, we achieve the new page rank for all nodes in the j-th block.
#Note that the function needs to save in memory
#k + 2 vectors of n/k elements:
#    one for the list of nodes in the j-th block
#    one for the new rank values of these nodes
#    k vectors to combine
def combine(nodes,vectors,s,n):
    tmp = dict()
    
    for j in nodes:
        tmp[j] = float(1-s)/n
        for i in range(len(vectors)):
            if j in vectors[i]:
                tmp[j] += vectors[i][j]
    
    return tmp

#This function implements the operation of computing the difference between the new and the old rank vector.
def verify(rank,tmp):
  diff = 0
  
  for i in rank.keys():
      diff += abs(rank[i]-tmp[i])
  
  return diff

def pageRank3(graph,degree,n,s,step,confidence,num_jobs):
  done = 0
  time = 0
  k=int(sqrt(num_jobs))
  
  #Each info about the nodes of graph is represented as a vector of k blocks.
  #Block[i] contains the info of nodes in the i-th subset.
  
  #Info: rank
  rank = []
  for i in range(k):
      rank.append(dict())
      for j in degree[i].keys():
          rank[i][j]=float(1)/n #Initial value
  
  #Info: temporary rank
  tmp=[]
  for i in range(k):
      tmp.append(dict())
    
  #Next instruction create a set of num_jobs processes and names this set parallel.
  #If you prefer to create threads in place of processes, you must write Parallel(n_jobs=num_jobs,backend="threading")
  with Parallel(n_jobs=num_jobs) as parallel:
      
      while not done and time < step:
          time += 1
          
          #Next instruction asks to the set of processes created above to run the function execute with the given parameters.
          #Note that they correspond to k^2 = num_jobs runs, one for each process.
          #It is possible to assign less or more runs than the number of processes.
          #In these cases there will processes that do nothing or others that do more job than others.
          #The output of each execution is saved in a vector:
          #the i-th entry of this vector contains the output of the i-th execution.
          #In our case, result[0] contains the output of execute when j=0 and i=0,
          #result[1] contains the output of execute when j=0 and i=1,
          #result[k] contains the output of execute when j=1 and i=0, and so on.
          results = parallel(delayed(execute)(graph[i][j],degree[i], rank[i],s) for j in range(k) for i in range(k))
          
          #Next instruction asks to the set of processes created above to run the function combine with the given parameters.
          tmp = parallel(delayed(combine)(list(degree[j].keys()),results[j*k:(j+1)*k],s,n) for j in range(k))
          
          diff = 0
          
          #Next instruction asks to the set of processes created above to run the function verify with the given parameters.
          differences = parallel(delayed(verify)(rank[i],tmp[i]) for i in range(k))
          
          for i in range(k):
              diff += differences[i]
              rank[i] = tmp[i].copy()
          
          if diff <= confidence:
              done = 1
    
  return time, rank

