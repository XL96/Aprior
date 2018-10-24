#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 22:45:48 2018

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

class Node:
    def __init__(self, Item,Parent,Count):
        self.Item = Item
        self.Children = []
        self.Parent = Parent
        self.Count = Count
        
def ItemCount(df, threshold):
    Items = {}
    for tuples in df:
        for item in tuples:
            if item not in Items:
                Items[item] = 1*df[tuples]
            else:
                Items[item] += 1*df[tuples]
    frequent = {}
    for keys in Items:
        if Items[keys] >= threshold:
            frequent[keys]=Items[keys]
    return frequent


def CreateTree(df,threshold):
    Frequent = ItemCount(df,threshold)
    Itemlist = sorted(Frequent,key=Frequent.get,reverse = True)
    Itemlistreverse = sorted(Frequent,key=Frequent.get)
    Header = {}
    for i in Itemlistreverse:
        Header[i] = []
    Root = Node('Null',None,1)
    for tuples in df:
        record = set(tuples)
        pattern = []
        for item in Itemlist:
            if item in record:
                pattern.append(item)
        UpdateTree(Root,pattern,Header,df[tuples])
   # PrintTree(Root)
    return Root, Header


def Mine_pattern(data,prefix,freq_pattern,threshold):
    root,header = CreateTree(data,threshold)
    for item in header:
        freq = set(prefix)
        freq.add(item)
        freq_pattern.append(freq)
        conditional_pattern = {}
        while header[item]!= []:
            if header[item] != []:
                path = []
                Prefix(header[item][0],path)
                #print(path)
                if len(path) > 1:
                    conditional_pattern[frozenset(path[1:])] = header[item][0].Count
                header[item].pop(0)
        Mine_pattern(conditional_pattern,freq,freq_pattern,threshold)

def Prefix(node,path):
    if node.Parent != None:
        path.append(node.Item)
        Prefix(node.Parent,path)
    
def UpdateTree(root,pattern,header,count):
    while pattern != []:
        item = pattern.pop(0)
        Inchildren = False
        for child in root.Children:
            if child.Item == item:
                child.Count += 1*count
                Inchildren = True
                root = child
        if Inchildren == False:
            leaf = Node(item,root,1*count)
            root.Children.append(leaf)
            header[item].append(leaf)
            root = leaf
            
def PrintTree(root):
    print(root.Item,root.Count)
    if root.Children != []:
        for child in root.Children:
            PrintTree(child)




if __name__ == "__main__":
    Unprepro = {}
    for tuples in df.itertuples():
        Unprepro[frozenset(tuples)] = 1    

    frequent = []
    Mine_pattern(Unprepro,set([]),frequent,32560/2)
    print(frequent)

    print()

    

