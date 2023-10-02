# Python program to create an undirected
# graph and add nodes and edges to a graph
 
# To import package
import networkx as nx
import matplotlib.pyplot as plt
from Algo.algo import FWAlgorithm

# To create an empty undirected graph
G = nx.DiGraph()
  
# To add a node
G.add_node(1,pos=(3,7))
G.add_node(2,pos=(7,7))
G.add_node(3,pos=(1,3))
G.add_node(4,pos=(4,1))
G.add_node(5,pos=(6,2))
#G.add_node(7,pos=(5,5))
#G.add_node(9,pos=(6,6))
  
# To add an edge
# Note graph is undirected
# Hence order of nodes in edge doesn't matter
G.add_edge(1,2,weight=5)
G.add_edge(1,4,weight=6)
G.add_edge(2,3,weight=1)
G.add_edge(5,1,weight=2)
G.add_edge(5,4,weight=5)
G.add_edge(3,1,weight=3)
G.add_edge(2,5,weight=7)
G.add_edge(3,4,weight=4)
G.add_edge(4,3,weight=2)
G.add_edge(4,5,weight=3)
#G.add_edge(9,1,weight=5)
#G.add_edge(1,7,weight=5)
#G.add_edge(2,9,weight=5)
  
# To get all the nodes of a graph
node_list = G.nodes()
print("#1")
print(node_list)
  
# To get all the edges of a graph
edge_list = G.edges()
print("#2")
print(edge_list)

#print(G[1][2])

pos=nx.get_node_attributes(G,'pos')
nx.draw(G,pos)
#nx.draw(G, with_labels=True, font_weight='bold')
labels = nx.get_edge_attributes(G,'weight')
#print(labels)
#{(1, 2): 5, (1, 4): 6, (2, 3): 1, (2, 5): 7, (3, 1): 3, (3, 4): 4, (4, 3): 2, (4, 5): 3, (5, 1): 2, (5, 4): 5}
fw_obj=FWAlgorithm()
#Create Adjacency Matrix and Initial Distance Matrix
fw_obj.initalize(labels,5)
#Run the FW Algo
fw_obj.compute_distance_matrix()
#nx.draw(G, with_labels=True, font_weight='bold')
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
#plt.show()

"""
# To remove a node of a graph
G.remove_node(3)
node_list = G.nodes()
print("#3")
print(node_list)
  
# To remove an edge of a graph
G.remove_edge(1,2)
edge_list = G.edges()
print("#4")
print(edge_list)
  
# To find number of nodes
n = G.number_of_nodes()
print("#5")
print(n)
  
# To find number of edges
m = G.number_of_edges()
print("#6")
print(m)
  
# To find degree of a node
# d will store degree of node 2
d = G.degree(2)
print("#7")
print(d)
 
# To find all the neighbor of a node
neighbor_list = G.neighbors(2)
print("#8")
print(neighbor_list)
 
#To delete all the nodes and edges
G.clear()
"""
