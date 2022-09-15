#
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import gzip
import sys
import re
import os
import gensim, logging
from optparse import OptionParser
import pickle

filename = "./file.txt"
blacklist = "./bl.txt"
word_regex=r'[^a-zA-Zéèçàêùôâ]'
colors=['r','g','b']
working_dir = "aa"

class wordseq:
    def __init__(self, f):
        self.f = f
        
    def __iter__(self):
        print ("Reading "+self.f),
        handler = open(self.f, "r", encoding="utf-8")
        alll = ""
        for line in handler:
            alll += line.strip()+" "

        for line in re.split(r'\.', alll):
            #print ("AAA"+line,)
            words = re.split(word_regex, line)
            words = [clean_word(x) for x in words]
            yield words
        handler.close()
            # for w in words:
            #     print ("AA"+w)

def clean_word(w):
    w = w.lower()
    w = re.sub('s$','',w)
    return w
            
def load_bl(blacklist):
    res = []
    handler = open (blacklist, "r", encoding="utf-8")
    for line in handler:
        res.append(line.strip())
        print ("BLLLLL: "+line)
    return res
            
def do_occurence(filename):
    occ = {}
    handler = open(filename, "r", encoding="utf-8")
    for line in handler:
        words = re.split(word_regex, line)
        words = [clean_word(x) for x in words]
        for w in words:
            if w in occ:
                occ[w] += 1
            else:
                occ[w] = 1
    return occ
            

def gen_graph (model, word, bl):
    G = nx.MultiDiGraph()
    gen_graph_r(model, word, 4, G, bl)
    print (G)
    return G


def gen_graph_r (model, word, depth, G, bl):
    if depth > 0:
        count = 0
        #print ("----\nMost similar for "+word)
        for s in model.wv.most_similar(positive=[word], topn=30):
            #print (s)
            #print (bl)
            if s[0] not in bl:
                count = count + 1
                G.add_edge(word, s[0], value=s[1], color=colors[depth%3] )
                gen_graph_r(model, s[0], depth-1, G, bl)
            if count >depth/1.5 + 2:
                break


def plot_graph(G, occ, root, working_dir):
    H = G#G.to_undirected()
    #pos = nx.kamada_kawai_layout(H)
    pos = nx.nx_agraph.graphviz_layout(G, prog="twopi", root=root)
    fig, ax = plt.subplots(figsize=(12, 12))
    edgewidth = 1
    nodesize = [occ[v] * 20 for v in H]
    # Visualize graph components
    edges = G.edges()
    ccolors = [G[u][v][0]['color'] for u,v in edges]
    nx.draw_networkx_edges(H, pos, alpha=0.3, width=edgewidth, edge_color=ccolors)
    nx.draw_networkx_nodes(H, pos, node_size=nodesize, node_color="#210070", alpha=0.9)
    label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
    nx.draw_networkx_labels(H, pos, font_size=8, bbox=label_options)
    fig.tight_layout()
    fig.savefig(working_dir+'/result.png', dpi=200)
    #plt.axis("off")
    #plt.show()

def print_most(occ, bl):
    count = 0
    max = 30
    for w in sorted (occ, key=occ.get, reverse=True):
        if w not in bl:
            count += 1
            if count == max:
                break
            print (w+ "("+str(occ.get(w))+")")

    
def main():
    parser = OptionParser()
    load=False
    parser.add_option("-f", "--file", action="store", type="string", dest="filename")
    parser.add_option("-b", "--blacklist", action="store", type="string", dest="blacklist")
    parser.add_option("-w", "--word", action="store", type="string", dest="word")
    parser.add_option("-d", "--directory", action="store", type="string", dest="dir")
    parser.add_option("-a", "--redoall", action="store_true", dest="redo")
    parser.add_option("-W", "--window", action="store", dest="window")
    parser.add_option("-e", "--epoch", action="store", dest="epoch")
    (options, args) = parser.parse_args()
    epoch = 10
    window = 5
    if options.window:
        window = options.window
    if options.epoch:
        epoch = options.epoch
    
    if options.filename:
        filename  = options.filename
        load=True

    if options.blacklist:
        print ("blacklist "+options.blacklist)
        blacklist = options.blacklist

    if options.dir:
        working_dir = options.dir

    if options.redo and options.dir:
        print ("redoing all")
        os.system("rm -f "+options.dir+"/all.txt")
        os.system("cat "+options.dir+"/*.txt > "+options.dir+"/all.txt")

    if load:
        seq = wordseq(working_dir+"/"+filename)
        model = gensim.models.Word2Vec(seq, min_count=2, window=int(window), vector_size=50, epochs=int(epoch))
        occ = do_occurence(working_dir+"/"+filename)
        print (occ)
        print ("Done.");
        model.save(working_dir+'/mymodel-300k')
        with open(working_dir+'/mymodel-occ', "wb") as outfile:
            pickle.dump(occ, outfile)
        
    #else:
    model = gensim.models.Word2Vec.load(working_dir+'/mymodel-300k')
    occ = {}
    with open(working_dir+"/mymodel-occ", "rb") as infile:
        occ = pickle.load (infile)

        #print(model.wv.distance('homme','pouvoir'))
        #print(model.wv.distance('femme','pouvoir'))
        #print(model.wv.doesnt_match("bateau maison porte rue".split()))
    if options.word:
        my_bl = load_bl(blacklist)
        print_most (occ, my_bl)
        print (options.word)
        print ( model.wv.most_similar(positive=[options.word], topn=10))
        print ("AAAAAAAAAAA")
            #print ( model.wv.most_similar(positive=["parent", "parents"], negative=["mère","mères","femme","femmes"], topn=10))
            #print ( model.wv.most_similar(positive=["parent", "parents"], negative=["pères","homme","hommes"], topn=10))
        graph = gen_graph(model, options.word, my_bl)
        plot_graph(graph, occ, options.word, working_dir)
        #print (model.wv.most_similar(positive=['homme'], topn=10))
        #print (model.wv.most_similar(positive=['femme'], topn=10))

if __name__ == "__main__":
    main()
