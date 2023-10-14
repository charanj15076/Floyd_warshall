import networkx as nx
import osmnx as ox
from itertools import islice

# this returns a network graph of paths where the source is in the center
def generate_graph_from_centroid(source_latitude, source_longtitude, distance_meter):
    source_point = source_latitude, source_longtitude

    # Download the street network graph for the specified area
    graph = ox.graph_from_point(source_point, dist=distance_meter, network_type='all')

    return graph


# this removes blockages in a graph
def remove_blocked_nodes(graph, blockages_list):
    for blockage_node in blockages_list:
        blockage_node = ox.distance.nearest_nodes(graph, blockage_node['lng'], blockage_node['lat'])
        try:
            graph.remove_node(blockage_node)
        except NetworkXError:
            # if node isn't there just ignore it
            pass
    return graph


# this returns nodes & edges as geodataframes from a graph
def convert_to_gdf(graph):
    # paths = dict(nx.all_pairs_shortest_path(graph))

    gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

    return gdf_nodes, gdf_edges


# this is the distance matrix used by fwa
def get_input_distance_matrix(graph, source_latitude, source_longtitude):
    source_point = source_latitude, source_longtitude
    source_node = ox.distance.nearest_nodes(graph, source_point[1], source_point[0])
    all_nodes = [v for v, d in graph.out_degree()]
    
    all_paths = []
    for target_node in all_nodes:
        paths = list(nx.all_simple_paths(graph, source=source_node, target=target_node, cutoff=20))
        all_paths.extend(paths)

    # Fill in the distance matrix with actual distances between nodes
    distance_matrix = {}
    for path in all_paths:
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i + 1]

            edge_data = graph.get_edge_data(node1, node2, 0)
            if edge_data:
                distance = edge_data['length']  
                distance_matrix[node1,node2] = distance

    return distance_matrix


# get shortest paths form a source and destination
def get_n_shortest_paths(blockages_list, source_latitude, source_longtitude, destination_latitude, destination_longitude, n):
    source_point = source_latitude, source_longtitude
    destination_point = destination_latitude, destination_longitude

    north = max(source_latitude, destination_latitude)
    south = min(source_latitude, destination_latitude) 
    west = min(source_longtitude, destination_longitude)
    east = max(source_longtitude, destination_longitude)

    # Download the street network graph for the specified area
    # graph = ox.graph_from_bbox(north, south, east, west, network_type='all')
    graph = ox.graph_from_point(source_point, dist=5000, network_type='all')
    graph = remove_blocked_nodes(graph, blockages_list)

    source = ox.distance.nearest_nodes(graph, source_point[1], source_point[0])
    target = ox.distance.nearest_nodes(graph, destination_point[1], destination_point[0])

    n_shortest_paths = list(ox.routing.k_shortest_paths(graph, source, target, k=n))

    routes_list = []
    for path in n_shortest_paths:
        gdf_edge = ox.utils_graph.route_to_gdf(graph, path, weight='length')
        routes_list.append(gdf_edge)

    return routes_list

    
