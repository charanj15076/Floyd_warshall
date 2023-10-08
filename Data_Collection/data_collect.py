import networkx as nx
import pandas as pd
import osmnx as ox
ox.config(use_cache = True,log_console= True)

def data_collect(city_name,source_latitude,source_longtitude,destination_latitude,destination_longitude,distance_meter):
    #Start
    G = ox.graph_from_place("Fullerton,California,USA",network_type = 'all')
    G = ox.speed.add_edge_speeds(G)
    G = ox.speed.add_edge_travel_times(G)
    nodes, edges = ox.graph_to_gdfs(G)

    values_to_drop = 'NaN'

    edges = edges[edges['name'] != 'NaN']

    edges2 = edges.copy()

    edges_dataframe = pd.DataFrame(edges2.drop(columns='geometry'))

    column_name = 'name'
    edges_dataframe2 = edges_dataframe.dropna(subset=[column_name])

    #print(edges_dataframe['name'])

    source_point = (source_latitude, source_longtitude) 
 
    destination_point = (destination_latitude, destination_longitude)

    # Download the street network graph for the specified area
    graph = ox.graph_from_point(source_point, dist=distance_meter, network_type='all')

    # Find the nearest network nodes to the source and destination points
    source_node = ox.distance.nearest_nodes(graph, source_point[1], source_point[0])
    #print(source_node)
    destination_node = ox.distance.nearest_nodes(graph, destination_point[1], destination_point[0])
    #print(destination_node)

    # Find the shortest path between the source and destination nodes
    shortest_path = nx.shortest_path(graph, source_node, destination_node, weight='length')

    # Extract all nodes along the shortest path
    nodes_between_source_and_destination = graph.subgraph(shortest_path)

    # distance_matrix = dict(nx.all_pairs_dijkstra_path_length(nodes_between_source_and_destination,weight='length'))

    all_paths = list(nx.all_simple_paths(graph, source=source_node, target=destination_node,cutoff = 20))

    num_nodes = len(graph.nodes)
    # [[float('inf')] * num_nodes for _ in range(num_nodes)]
    distance_matrix = {}

    # Fill in the distance matrix with actual distances between nodes
    for path in all_paths:
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i + 1]

            edge_data = graph.get_edge_data(node1, node2, 0)
    #         print(edge_data)
            if edge_data:
                distance = edge_data['length']  
    #               print(distance)
                distance_matrix[node1,node2] = distance
    #for row in distance_matrix:
    #    print(row)

    return distance_matrix
