import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
# import PIL.ImageOps
# from PIL import Image
import numpy as np
import itertools
import math
import sys
import os
from scipy.spatial.distance import squareform
def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s
class Config():
    colors = ['aquamarine', 'darkorange', 'blanchedalmond', 'blueviolet', 'brown',
              'burlywood', 'cadetblue', 'chartreuse','chocolate', 'coral',
              'cornflowerblue', 'cornsilk', 'crimson', 'darkblue', 'darkcyan',
              'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki',
              'darkmagenta', 'darkolivegreen', 'bisque', 'darkslateblue',
              'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
              'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet',
              'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue',
              'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
              'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow',
              'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory'] + ['black'] *100

def dismat_calculator(array):
    print("Calculating...")
    for i in range(len(array)):
        vector1 = np.array(array[i])
        for j in range(i+1,len(array)):
            vector2 = np.array(array[j])
            vector3 = []
            for z in range(len(vector1)):
                vector3.append(min(vector1[z],vector2[z]))
            dist = 1 - np.linalg.norm(vector3)/(np.linalg.norm(vector1) * np.linalg.norm(vector2))**0.5
            dismat[i][j] = dist
            dismat[j][i] = dist
    print("Calculation done")
    print(dismat)
    return dismat

def matrix_reader(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.readlines()
    row = len(content)
    column = len(content[0].split(' '))
    tar_np = np.zeros((row, column))
    for each_row in range(row):
        curr_row = content[each_row].split(' ')
        for each_column in range(column):
            tar_np[each_row][each_column] = float(curr_row[each_column])
    return tar_np

def tag_reader(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')
    row = len(content)
    column = len(content[0].split(' '))
    tags = []
    for each_row in range(row):
        curr_row = content[each_row].split('\t')
        tags.append(curr_row[1:])
    tags = tags[1:]
    for i in range(len(tags)):
        tags[i] = ",".join(tags[i])
        tags[i] = str(i) + tags[i]
    return tags

def make_graph(sim, labels=None):
    G = nx.Graph()
    for (i, j) in [(i, j) for i in range(sim.shape[0]) for j in range(sim.shape[1]) if i != j and sim[i,j] != 0]:
        if labels == None:
            G.add_edge(i, j, weight=sim[i,j])
        else:
            G.add_edge(labels[i], labels[j], weight=sim[i,j])
    return G

def save_matrix(dismat):
    with open('dismat_matrix.txt', 'w', encoding='utf-8') as f:
        write_content = ''
        row = len(dismat)
        for i in range(row):
            eachline = ''
            column = len(dismat[0])
            for j in range(len(dismat[0])):
                eachline += str(dismat[i][j])
                if j != len(dismat[0])-1: eachline += ' '
            write_content += eachline
            if i != row-1 : write_content += '\n'
        f.write(write_content)
def analysis(dismat):
    dismatflat = dismat.reshape((-1,))
    dismatflat = dismatflat[dismatflat != 0]  # Too many ones result in a bad histogram so we remove them
    plt.figure(figsize=(15, 10))
    _ = plt.hist(dismatflat, bins=200)
    plt.show()
    mmax = np.max(dismatflat)
    mmin = np.min(dismatflat)
    mmean = np.mean(dismatflat)
    mstd = np.std(dismatflat)
    print('avg={0:.2f} min={1:.2f} max={2:.2f} mstd={3:.2f}'.format(mmean, mmin, mmax, mstd))
    for i in range(len(dismat)):
        for j in range(len(dismat)):
            dismat[i][j] = 1 - sigmoid((dismat[i][j] - mmean)/ mstd)
            # dismat[i][j] = (dismat[i][j] - mmean) / mstd
    print(dismat)
    dismatflat = dismat.reshape((-1,))
    dismatflat = dismatflat[dismatflat != 0]  # Too many ones result in a bad histogram so we remove them
    plt.figure(figsize=(15, 10))
    _ = plt.hist(dismatflat, bins=200)
    plt.show()
    mmax = np.max(dismatflat)
    mmin = np.min(dismatflat)
    mmean = np.mean(dismatflat)
    mstd = np.std(dismatflat)
    print('avg={0:.2f} min={1:.2f} max={2:.2f} mstd={3:.2f}'.format(mmean, mmin, mmax, mstd))
    return dismat
def community_maker(dismat,threshold,tags=None):
    adjmat = dismat.copy()
    np.fill_diagonal(adjmat,
                     np.min(dismat))  # Set the diagonal elements to a small value so that they won't be zeroed out
    adjmat = adjmat.reshape((-1,))
    adjmat[adjmat > threshold] = 0
    # adjmat[adjmat > 0] = 1
    print("{} out of {} values set to zero".format(len(adjmat[adjmat == 0]), len(adjmat)))
    adjmat = adjmat.reshape(dismat.shape)
    #
    G = make_graph(adjmat,labels=tags)
    # G = make_graph(adjmat)
    print(len(G.nodes))
    plt.figure(figsize=(17, 15))
    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    plt.show()
    #
    from networkx.algorithms.community.centrality import girvan_newman
    from networkx.algorithms.community.label_propagation import label_propagation_communities, asyn_lpa_communities


    comp = girvan_newman(G)
    max_shown = 3
    shown_count = 1
    possibilities = []
    for communities in itertools.islice(comp, max_shown):
        print("Possibility", shown_count, ": ", end='')
        print(communities)
        print(len(communities))
        print([len(c) for c in communities if len(c) >= 10 ])
        possibilities.append(communities)
        color_map = ["" for x in range(len(G))]
        color = 0
        for c in communities:
            indices = [i for i, x in enumerate(G.nodes) if x in c]
            for i in indices:
                color_map[i] = Config.colors[color]
            color += 1
        plt.figure(figsize=(17, 15))
        pos = nx.spring_layout(G)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        nx.draw(G, pos, node_color=color_map, with_labels=True)
        plt.savefig('Graph1-{}.png'.format(shown_count))
        plt.show()
        shown_count += 1

def data_reader(filename,num = 125):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')[1:]
        l = list(map(lambda x: x.strip().split('\t')[1:], data))[:num]
    array = np.array(l, dtype = 'float')
    return array

num = 125
array = data_reader('user_book_tag.csv',num)
dismat = np.zeros((len(array),len(array)))
# tags = tag_reader('user_3tag_by_book.csv')
tags = []
for i in range(num):
    tags.append(i)
print(tags)

# dismat = matrix_reader('dismat_matrix.txt')
# print(dismat)

dismat = dismat_calculator(array)
# analysis(dismat)
print(dismat)

# save_matrix(dismat)
# 0.16+
community_maker(dismat,0.155,tags)
# community_maker(dismat,0.05)