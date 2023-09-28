"""
To-Do:
1. Apply a distance path list for each vertex
2. Check for any further improvements.
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
        self.path_matrix=[[list() for j in range(self.number_of_vertex)] for i in range(self.number_of_vertex)]
        for i in range(self.number_of_vertex):
            self.distance_matrix[i][i]=0
            self.path_matrix[i][i].append(i+1)
        for i in edge_dict:
            edges=list(int(j)-1 for j in i.split(','))
            self.distance_matrix[edges[0]][edges[1]]=edge_dict[i]

            edges_1=[i+1 for i in edges]
            self.path_matrix[edges[0]][edges[1]]=edges_1
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
                        self.path_matrix[i][j]=[i+1]
                        self.path_matrix[i][j].extend(self.path_matrix[k][j])

        self.display_distance_matrix()
        self.display_path_matrix()

        #Check for negative cycles
        for k in range(self.number_of_vertex):
            if self.distance_matrix[k][k]<0:
                        raise NegativeCycleError("Negative Cycle Detected")
