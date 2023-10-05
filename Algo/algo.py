"""
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

#Recompute distance matrix by removing multiple edges
#Input a list of tuples, each tuple representing an edge
#Remember: Edge must be part of the graph!
fw_obj.remove_edges([(3,4),(2,5),(2,3)])

#Add matrices back to the graph
#Input a list of tuples, each tuple representing an edge
#Remember: Edge must be part of the graph!
fw_obj.add_edges([(2,3),(2,5),(3,4),(3,1)])
"""
import copy

#Define Infinity
INFINITY = 100000

class NegativeCycleError(Exception):
    pass

class FWAlgorithm:
    """
    dict={"1,2":5,"3,4":4}
    """
    def __init__(self):
        #Store the distance any pair of vertices
        self.distance_matrix=list()
        self.path_matrix=list()
        self.number_of_vertex=0
        #Store the inital graph state. Helpful in removing edges.
        self.adjacency_matrix=list()
        #Store deleted edges. Helpful in removing edges.
        self.deleted_edges=list()
        
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
        
        #Initialize the path matrix
        self.path_matrix=[[list() for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        
        for i in range(self.number_of_vertex):
            self.distance_matrix[i][i]=0
            self.path_matrix[i][i].append(i+1)
            
        for edge in edge_dict:
            self.distance_matrix[edge[0]-1][edge[1]-1]=edge_dict[edge]
            
            self.path_matrix[edge[0]-1][edge[1]-1].extend([edge[0],edge[1]])

        self.adjacency_matrix=copy.deepcopy(self.distance_matrix)

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
                        self.path_matrix[i][j]=self.path_matrix[i][k]+self.path_matrix[k][j][1:]

            self.display_distance_matrix()
            self.display_path_matrix()
            
        #Check for negative cycles
        for k in range(self.number_of_vertex):
            if self.distance_matrix[k][k]<0:
                        raise NegativeCycleError("Negative Cycle Detected")

        #self.path_matrix_backup=copy.deepcopy(self.path_matrix)
        #self.display_distance_matrix()
        #self.display_path_matrix()

    def remove_edges(self,delete_edges):

        affected_edges=[]
        #Delete direct edges and add them to edges affected
        for k in delete_edges:
            self.deleted_edges.append(k)

            #Find all paths that used the deleted edges and retrace their paths    
            for i in range(self.number_of_vertex):
                for j in range(self.number_of_vertex):
                    if str(self.path_matrix[i][j])[1:-1].find(str(k)[1:-1])>=0:
                        print("This path ",i+1," to ",j+1," needs to be reworked")
                        #self.distance_matrix[i][j]=INFINITY
                        #self.path_matrix[i][j].clear()
                        if (i+1,j+1) in self.deleted_edges:
                            print(i+1,',',j+1,'already deleted')
                            self.distance_matrix[i][j]=INFINITY
                            self.path_matrix[i][j].clear()
                            self.display_distance_matrix()
                            self.display_path_matrix()
                        else:
                            self.path_matrix[i][j]=[i+1,j+1]
                            print(i+1,',',j+1,'adjacency matrix')
                            self.distance_matrix[i][j]=self.adjacency_matrix[i][j]
                            #self.path_matrix[i][j].clear()
                            #self.distance_matrix[i][j]=INFINITY
                            self.display_distance_matrix()
                            self.display_path_matrix()
                        affected_edges.append([i,j])

            #Delete the edge
            #self.distance_matrix[k[0]-1][k[1]-1]=INFINITY
            #print(k[0],k[1])
            #self.path_matrix[k[0]-1][k[1]-1].clear()
                           
        print("Affected edges: ",affected_edges)

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
                        print("Computing for edges ",i+1,j+1)
                        self.distance_matrix[i][j]=self.distance_matrix[i][k]+self.distance_matrix[k][j]
                        self.path_matrix[i][j]=self.path_matrix[i][k]+self.path_matrix[k][j][1:]

            
            self.display_distance_matrix()
            self.display_path_matrix()
           
    def add_edges(self,edges_to_add):

        for k in edges_to_add:
            #Remove from Deleted Edge list
            self.deleted_edges.remove(k)
            print("Attempting to add: ",k)
            if self.distance_matrix[k[0]-1][k[1]-1]<=self.adjacency_matrix[k[0]-1][k[1]-1]:
                continue

            #self.distance_matrix[k[0]-1][k[1]-1]=self.adjacency_matrix[k[0]-1][k[1]-1]
            #self.path_matrix[k[0]-1][k[1]-1]=[k[0],k[1]]
            #Rows
            for i in range(self.number_of_vertex):
                if self.distance_matrix[i][k[0]-1]==INFINITY:
                    continue
                
                for j in range(self.number_of_vertex):
                    if i==j or self.distance_matrix[k[1]-1][j]==INFINITY:
                        continue

                    if self.distance_matrix[i][k[0]-1]+self.adjacency_matrix[k[0]-1][k[1]-1]+self.distance_matrix[k[1]-1][j]<self.distance_matrix[i][j]:
                        print("For ",i+1,"->",j+1,":",self.distance_matrix[i][k[0]-1],'+',self.adjacency_matrix[k[0]-1][k[1]-1],'+',self.distance_matrix[k[1]-1][j],'<',self.distance_matrix[i][j])
                        self.distance_matrix[i][j]=self.distance_matrix[i][k[0]-1]+self.adjacency_matrix[k[0]-1][k[1]-1]+self.distance_matrix[k[1]-1][j]
                        self.path_matrix[i][j]=self.path_matrix[i][k[0]-1]+[k[1]]+self.path_matrix[k[1]-1][j][1:]

            self.display_distance_matrix()
            self.display_path_matrix()

        """
        edges_to_try=[]
        #Adding all edges that could have a path in the added edges
        #Assigning default values
        for k in edges_to_add:
            for i in range(self.number_of_vertex):
                for j in range(self.number_of_vertex):
                    if str(self.path_matrix_backup[i][j])[1:-1].find(str(k)[1:-1])>=0:
                       print("This path ",i+1," to ",j+1," could use the new path")
                       if k not in edges_to_try:
                           #self.path_matrix[i][j]=self.path_matrix_backup[i][j]
                           #self.distance_matrix[i][j]=self.adjacency_matrix[i][j]
                           edges_to_try.append([i,j])

            #Add the edge
            self.distance_matrix[k[0]-1][k[1]-1]=self.adjacency_matrix[k[0]-1][k[1]-1]
            self.path_matrix[k[0]-1][k[1]-1]=[k[0],k[1]]
                           
        print("Edges that can possibly be added: ",edges_to_try)

        #Computing Intermediate Distance Matrix for all possible edges
        for k in range(self.number_of_vertex):
            print("For Iteration ",(k+1))
            #Rows
            for i in range(self.number_of_vertex):
                for j in range(self.number_of_vertex):
                    #Avoid unaffected edges
                    if [i,j] not in edges_to_try:
                        continue
                    
                    if (self.distance_matrix[i][k]+self.distance_matrix[k][j]) < self.distance_matrix[i][j]:
                        print("Computing for edges ",i,j)
                        self.distance_matrix[i][j]=self.distance_matrix[i][k]+self.distance_matrix[k][j]
                        self.path_matrix[i][j]=self.path_matrix[i][k]+self.path_matrix[k][j][1:]

        print(edges_to_try)
        """
