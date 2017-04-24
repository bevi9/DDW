import nltk
import csv
import networkx as nx
import matplotlib.pyplot as plt
import pylab
from networkx.algorithms import *
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.algorithms.centrality import *
import itertools

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

G=nx.Graph()
actors = []

with open('casts.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=';')
	movie = 'Batman'
	movie_actors = []
	for row in spamreader:
		if row[2] not in actors:
			actors.append(row[2])
			G.add_node(row[2])
		if movie == row[1]:
			for a in movie_actors:
				G.add_edge(a,row[2])
		else:
			movie = row[1]
			movie_actors = []
		movie_actors.append(row[2])

print "Nodes:",nx.number_of_nodes(G)
print "Edges:",nx.number_of_edges(G)
print "Density:",nx.density(G)
if(nx.is_connected(G)): print("Graph connected")
else: print("Graph disconnected")

c = [degree_centrality, eigenvector_centrality]
for cen in c:
	best = 0
	top = []
	ce = cen(G)
	for i in range(1,10):
		best = max(ce, key=ce.get)
		ce.pop(best,None)
		top.append(best)
	print(top)

best = 0
top_clusters = []
c = clustering(G)
for i in range(1,10):
    best = max(c, key=c.get)
    c.pop(best,None)
    top_clusters.append(best)
print("avg clustering: ",average_clustering(G))
print(top_clusters)

nx.write_gexf(G,"graph.gexf")

# visualise
def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

#Assuming that the graph g has nodes and edges entered
#save_graph(G,"my_graph.pdf")
