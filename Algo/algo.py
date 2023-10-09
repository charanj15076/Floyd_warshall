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

#Pass the graph
fw_obj.initalize(sample_dictionary)

#Compute distance matrix
fw_obj.compute_distance_matrix()
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
        self.mapping=dict()
        #Store the inital graph state. Helpful in removing edges.
        self.adjacency_matrix=list()
        #Store deleted edges. Helpful in removing edges.
        self.deleted_edges=list()
        
    def display_distance_matrix(self):
        print(" ",end='\t')
        for vertex in range(1,self.number_of_vertex+1):
            print(self.mapping[vertex],end='\t')
        print()
        #row=1
        distance=dict()
        for i in range(self.number_of_vertex):
            print(self.mapping[i+1],end='\t')
            #row+=1
            for j in range(self.number_of_vertex):
                print(self.distance_matrix[i][j],end='\t')
                distance[(self.mapping[i+1],self.mapping[j+1])]=self.distance_matrix[i][j]
            print()
        print()
        return distance

    def display_path_matrix(self):
        print(" ",end='\t')
        for vertex in range(1,self.number_of_vertex+1):
            print(self.mapping[vertex],end='\t')
        print()
        paths=dict()
        #row=1   
        for i in range(self.number_of_vertex):
            print(self.mapping[i+1],end='\t')
            #row+=1
            for j in range(self.number_of_vertex):
                print(self.path_matrix[i][j],end='\t')
                paths[(self.mapping[i+1],self.mapping[j+1])]=self.path_matrix[i][j]
            print()
        print()
        return paths

    #Returns the initial distance matrix and path matrix in a dictionary format
    def initalize(self,edge_dictionary):
        global INFINITY
        edge_dict=dict()
        #{1:986532,2:244211}
        #Intialize the number of vertices
        vertex_count=1
        for k in edge_dictionary:
            if k[0] not in self.mapping.values():
                self.mapping[vertex_count]=k[0]
                vertex_count+=1
            if k[1] not in self.mapping.values():
                self.mapping[vertex_count]=k[1]
                vertex_count+=1
            edge_dict[((list(self.mapping.keys())[list(self.mapping.values()).index(k[0])]),(list(self.mapping.keys())[list(self.mapping.values()).index(k[1])]))]=edge_dictionary[k]
        
        self.number_of_vertex=vertex_count-1

        #Change the number to a large integer
        #Initialize the distance matrix
        self.distance_matrix=[[INFINITY for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        
        #Initialize the path matrix
        self.path_matrix=[[list() for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]

        for i in range(self.number_of_vertex):
            self.distance_matrix[i][i]=0
            self.path_matrix[i][i].append(self.mapping[i+1])
            
        for edge in edge_dict:
            self.distance_matrix[edge[0]-1][edge[1]-1]=edge_dict[edge]
            
            self.path_matrix[edge[0]-1][edge[1]-1].extend([self.mapping[edge[0]],self.mapping[edge[1]]])

        self.adjacency_matrix=copy.deepcopy(self.distance_matrix)

        print("Initial Distance Matrix")
        yield self.display_distance_matrix()

        print("Initial Path Matrix")
        yield self.display_path_matrix()
        #return self.display_distance_matrix(),self.display_path_matrix()

    #Returns the actual distance matrix and path matrix in a dictionary format
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
        yield self.display_distance_matrix()
        yield self.display_path_matrix()

    def remove_edges(self,delete_edges):

        #delete_edges=[(list(self.mapping.keys())[list(self.mapping.values()).index(k[0])],list(self.mapping.keys())[list(self.mapping.values()).index(k[1])]) for k in delete_edges]
        affected_edges=[]
        #Delete direct edges and add them to edges affected
        for k in delete_edges:
            self.deleted_edges.append(k)

            #Find all paths that used the deleted edges and retrace their paths    
            for i in range(self.number_of_vertex):
                for j in range(self.number_of_vertex):
                    if str(self.path_matrix[i][j])[1:-1].find(str(k)[1:-1])>=0:
                        print("This path ",self.mapping[i+1]," to ",self.mapping[j+1]," needs to be reworked")
                        #self.distance_matrix[i][j]=INFINITY
                        #self.path_matrix[i][j].clear()
                        if (self.mapping[i+1],self.mapping[j+1]) in self.deleted_edges:
                            print(self.mapping[i+1],',',self.mapping[j+1],'already deleted')
                            self.distance_matrix[i][j]=INFINITY
                            self.path_matrix[i][j].clear()
                            self.display_distance_matrix()
                            self.display_path_matrix()
                            self.adjacency_matrix[i][j]=INFINITY
                        else:
                            self.path_matrix[i][j]=[self.mapping[i+1],self.mapping[j+1]]
                            print(self.mapping[i+1],',',self.mapping[j+1],'adjacency matrix')
                            self.distance_matrix[i][j]=self.adjacency_matrix[i][j]
                            #self.path_matrix[i][j].clear()
                            #self.distance_matrix[i][j]=INFINITY
                            self.display_distance_matrix()
                            self.display_path_matrix()
                        affected_edges.append([self.mapping[i+1],self.mapping[j+1]])

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
                    if [self.mapping[i+1],self.mapping[j+1]] not in affected_edges:
                        continue
                    
                    if (self.distance_matrix[i][k]+self.distance_matrix[k][j]) < self.distance_matrix[i][j]:
                        print("Computing for edges ",self.mapping[i+1],self.mapping[j+1])
                        self.distance_matrix[i][j]=self.distance_matrix[i][k]+self.distance_matrix[k][j]
                        self.path_matrix[i][j]=self.path_matrix[i][k]+self.path_matrix[k][j][1:]

            
        yield self.display_distance_matrix()
        yield self.display_path_matrix()
           
    def add_edges(self,edges_to_add):
        #edges_to_add=[(list(self.mapping.keys())[list(self.mapping.values()).index(k[0])],list(self.mapping.keys())[list(self.mapping.values()).index(k[1])]) for k in edges_to_add]
        for k in edges_to_add:
            #Remove from Deleted Edge list
            edge=((list(self.mapping.keys())[list(self.mapping.values()).index(k[0])]),(list(self.mapping.keys())[list(self.mapping.values()).index(k[1])]))
            #print(edge)
            if k in self.deleted_edges:
                self.deleted_edges.remove(k)
            print("Attempting to add: ",k)
            if self.distance_matrix[edge[0]-1][edge[1]-1]<edges_to_add[k]:
                print("Not adding ",k," ,distance is already less")
                continue

            #self.distance_matrix[k[0]-1][k[1]-1]=self.adjacency_matrix[k[0]-1][k[1]-1]
            #self.path_matrix[k[0]-1][k[1]-1]=[k[0],k[1]]
            if edges_to_add[k]<self.adjacency_matrix[edge[0]-1][edge[1]-1]:
                self.adjacency_matrix[edge[0]-1][edge[1]-1]=edges_to_add[k]
            
            #Rows
            for i in range(self.number_of_vertex):
                if self.distance_matrix[i][edge[0]-1]==INFINITY:
                    continue
                
                for j in range(self.number_of_vertex):
                    if i==j or self.distance_matrix[edge[1]-1][j]==INFINITY:
                        continue

                    if self.distance_matrix[i][edge[0]-1]+self.adjacency_matrix[edge[0]-1][edge[1]-1]+self.distance_matrix[edge[1]-1][j]<self.distance_matrix[i][j]:
                        print("For ",self.mapping[i+1],"->",self.mapping[j+1],":",self.distance_matrix[i][edge[0]-1],'+',self.adjacency_matrix[edge[0]-1][edge[1]-1],'+',self.distance_matrix[edge[1]-1][j],'<',self.distance_matrix[i][j])
                        self.distance_matrix[i][j]=self.distance_matrix[i][edge[0]-1]+self.adjacency_matrix[edge[0]-1][edge[1]-1]+self.distance_matrix[edge[1]-1][j]
                        self.path_matrix[i][j]=self.path_matrix[i][edge[0]-1]+[k[1]]+self.path_matrix[edge[1]-1][j][1:]

            yield self.display_distance_matrix()
            yield self.display_path_matrix()
