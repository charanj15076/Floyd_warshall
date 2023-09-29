"""
To-Do:
1. Apply for multiple paths removal
2. Add an implementation for addition of edges back to graph.

To run:
IMPORTANT: Don't make vertex value as 0. It throws index error. All vertices start from 1. Reason I've done this is so that it becomes easy to understand
distance matrices at each iteration. (I could improve on this but this is last in my list).
In a separate python file:
from Algo.algo import FWAlgorithm

#Create an object
fw_obj=FWAlgorithm()

#Create sample graph (or graph of the city as a dictionary)
#Keys reperesent the edge pairs separated by a comma.
#Value represents the edge weight.
sample_dictionary={"1,2":5,"1,4":6,"2,5":7,"2,3":1,"3,1":3,"3,4":4,"4,5":3,"4,3":2,"5,4":5,"5,1":2}

#Pass the graph and number of vertices to the method
fw_obj.initalize(sample_dictionary,5)

#Compute distance matrix
fw_obj.compute_distance_matrix()

#Recompute distance matrix by removing an edge
#Format is (starting vertex, ending vertex)
#Remember: Edge must be part of the graph!
fw_obj.recompute_distance_matrix(4,5)
"""

#Define Infinity
INFINITY = 100000

class NegativeCycleError(Exception):
    pass

class FWAlgorithm:
    """
    dict={"1,2":5,"3,4":4}
    """
    def __init__(self):
        self.distance_matrix=list()
        self.path_matrix=list()
        self.number_of_vertex=0
        self.adjacency_matrix=list()
        self.path_matrix_backup=list()
        
    def display_distance_matrix(self):
        print(" ",end='\t')
        for vertex in range(1,self.number_of_vertex+1):
            print(vertex,end='\t')
        print()
        row=1    
        for i in self.distance_matrix:
            print(row,end='\t')
            row+=1
            for j in i:
                print(j,end='\t')
            print()
        print()

    def display_path_matrix(self):
        print(" ",end='\t')
        for vertex in range(1,self.number_of_vertex+1):
            print(vertex,end='\t')
        print()
        row=1    
        for i in self.path_matrix:
            print(row,end='\t')
            row+=1
            for j in i:
                print(j,end='\t')
            print()
        print()
            
    def initalize(self,edge_dict,number_of_vertex):
        global INFINITY
        #Intialize the number of vertices
        self.number_of_vertex=number_of_vertex

        #Change the number to a large integer
        #Initialize the distance matrix
        self.distance_matrix=[[INFINITY for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        self.adjacency_matrix=[[INFINITY for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        self.path_matrix=[[list() for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        self.path_matrix_backup=[[list() for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        for i in range(self.number_of_vertex):
            self.distance_matrix[i][i]=0
            self.path_matrix[i][i].append(i+1)
            
        for i in edge_dict:
            edges=list(int(j)-1 for j in i.split(','))
            self.distance_matrix[edges[0]][edges[1]]=edge_dict[i]
            self.adjacency_matrix[edges[0]][edges[1]]=edge_dict[i]

            #edges_1=[i+1 for i in edges]
            self.path_matrix[edges[0]][edges[1]].append(edges[0]+1)
            self.path_matrix[edges[0]][edges[1]].append(edges[1]+1)
            self.path_matrix_backup[edges[0]][edges[1]]=self.path_matrix[edges[0]][edges[1]]

        print("Initial Distance Matrix")
        self.display_distance_matrix()

        print("Initial Path Matrix")
        self.display_path_matrix()

    def compute_distance_matrix(self):
        #Intermediate Distance Matrix
        for k in range(self.number_of_vertex):
            print("For Iteration ",(k+1))
            #Rows
            for i in range(self.number_of_vertex):
                for j in range(self.number_of_vertex):
                    #Avoid Useless Relexation attempt
                    if self.distance_matrix[i][k]==INFINITY or self.distance_matrix[k][j]==INFINITY:
                        print("Avoiding useless relaxation attempt for",i+1,j+1)
                        continue
                    
                    if (self.distance_matrix[i][k]+self.distance_matrix[k][j]) < self.distance_matrix[i][j]:
                        self.distance_matrix[i][j]=self.distance_matrix[i][k]+self.distance_matrix[k][j]
                        #self.path_matrix[i][j]=[i+1]
                        #self.path_matrix[i][j].extend(self.path_matrix[k][j])
                        self.path_matrix[i][j]=self.path_matrix[i][k]+self.path_matrix[k][j][1:]

            self.display_distance_matrix()
            self.display_path_matrix()
            
        #Check for negative cycles
        for k in range(self.number_of_vertex):
            if self.distance_matrix[k][k]<0:
                        raise NegativeCycleError("Negative Cycle Detected")

        #self.display_distance_matrix()
        #self.display_path_matrix()

    def recompute_distance_matrix(self,origin_vertex,destination_vertex):

        deleted_edge=[origin_vertex,destination_vertex]
        print("Edge to be deleted: ",deleted_edge)

        affected_edges=[]

        #Reset all affected paths
        #Reset all distances to INFINITY for affected edges
        for i in range(self.number_of_vertex):
            for j in range(self.number_of_vertex):
                if str(self.path_matrix[i][j])[1:-1].find(str(deleted_edge)[1:-1])>=0:
                   print("This path ",i+1," to ",j+1," needs to be reworked")
                   self.path_matrix[i][j]=self.path_matrix_backup[i][j]
                   self.distance_matrix[i][j]=self.adjacency_matrix[i][j]
                   affected_edges.append([i,j])
        print("Affected edges: ",affected_edges)
        
        #Delete the edge
        self.distance_matrix[origin_vertex-1][destination_vertex-1]=INFINITY
        self.path_matrix[origin_vertex-1][destination_vertex-1].clear()

        #Computing Intermediate Distance Matrix for affected edges
        for k in range(self.number_of_vertex):
            print("For Iteration ",(k+1))
            #Rows
            for i in range(self.number_of_vertex):
                for j in range(self.number_of_vertex):
                    #Avoid unaffected edges
                    if [i,j] not in affected_edges:
                        continue
                    
                    if (self.distance_matrix[i][k]+self.distance_matrix[k][j]) < self.distance_matrix[i][j]:
                        print("Computing for edges ",i,j)
                        self.distance_matrix[i][j]=self.distance_matrix[i][k]+self.distance_matrix[k][j]
                        self.path_matrix[i][j]=self.path_matrix[i][k]+self.path_matrix[k][j][1:]
        
        self.display_distance_matrix()
        self.display_path_matrix()
