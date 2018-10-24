#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 22:52:49 2018

@author: lixiang
"""

import pandas as pd
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'
df = pd.read_csv(url)
data = pd.read_csv('adult.data.csv',names=['age','workclass','fnlwgt','Education','education-num',
                                             'marital status','occupation','relationship','race','sex',
                                             'capital gain','capital loss','hours-per-week','country','income'],
                                            index_col=False)

data['hours-per-week'] = data['hours-per-week'].astype(str)
data['hours-per-week']= data['hours-per-week']+'hours'
data['capital gain'] = data['capital gain'].astype(str)
data['capital gain'] = data['capital gain']+'gain'
data['capital loss'] = data['capital loss'].astype(str)
data['capital loss'] = data['capital loss']+'loss'

def GenFrequent1(df, threshold):
    Items = {}
    for tuples in df.itertuples():
        for item in tuples:
            if item not in Items:
                Items[item] = 1
            else:
                Items[item] += 1
    frequent = []
    for keys in Items:
        if Items[keys] >= threshold:
            frequent.append(frozenset([keys]))
    return frequent
    
def Scan(df,C, threshold): #take list of candidates and return a list of frequent sets 
    count = {}
    for tuples in df.itertuples():
        record = set(tuples)
        for cand in C:
            if cand.issubset(record):         
                if cand not in count:
                    count[cand] = 1
                else:
                    count[cand] += 1
    Frequent = []
    for key in count:
        if count[key] >= threshold:
           Frequent.append(key)
    return Frequent

def GenCk(C,k): #Generate a list k item candidates
    Ck = []
    for i in range(len(C)):
        for j in range(i+1,len(C)):
            list1 = list(C[i])[:k-2]
            list2 = list(C[j])[:k-2]
            if list1 == list2:
                Ck.append(frozenset(C[i]|C[j]))
    return Ck

def Apriori(df,threshold):
    FrequentItemSets = []
    F1 = GenFrequent1(df,threshold)
    FrequentItemSets.append(F1)
    Candidate = GenCk(F1,2)
    k = 2
    while(len(Candidate)>0):
        Frequent = Scan(df,Candidate,threshold)
        FrequentItemSets.append(Frequent)
        k += 1
        Candidate = GenCk(Frequent,k)
    print('Frequent Itemsets with minimum support of: ',threshold)
    print()
    for i in range(len(FrequentItemSets)-1):
        print('Frequent',i+1,'Itemset:')
        for k in FrequentItemSets[i]:
            print(k)
        print()

if __name__ == "__main__":
    print(Apriori(df,32560/2))

