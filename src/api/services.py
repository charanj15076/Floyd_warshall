from data_collection import *
from fwa import FWAlgorithm

import osmnx



# Get all shortest paths from all locations in a centroid coordinate
# Input: center coordinates, list of blockage coordinates, distance
# Output: shortest distance & path matrices
def run_simulation(blockages_list, lat_center, lng_center, distance):

	G = generate_graph_from_centroid(lat_center, lng_center, distance)

	# remove blockages
	G = remove_blocked_nodes(G, blockages_list)

	nodes, edges = convert_to_gdf(G)
	distance_matrix = get_input_distance_matrix(G, lat_center, lng_center)

	fw_obj = FWAlgorithm()
	path_dict = fw_obj.initalize(distance_matrix)

	relaxations, path_dict = fw_obj.compute_distance_matrix()

	# merge all edges into one
	edge_list = []
	for source_node in path_dict:
		for destination_node in path_dict[source_node]:
			route = path_dict[source_node][destination_node]
			if route != []:
				gdf_edge = osmnx.utils_graph.route_to_gdf(G, route, weight='length')
				#edge_list = pd.concat([edge_list, gdf_edge])drop_duplicates()
				edge_list.append(gdf_edge)

	# df = edge_list[0]
	# for d in edge_list[1:]:
	# 	df = df.concat([df, d]).drop_duplicates().reset_index(drop=True)

	return edge_list


# Get 5 shortest paths to destination while considering blockages
# Input: blockages list, source and destination coordinates
# Output: 5 shortest paths
def get_shortest_paths(blockages_list, source_lat, source_lng, dest_lat, dest_lng):
	paths_list = get_n_shortest_paths(blockages_list, source_lat, source_lng, dest_lat, dest_lng, 5)

	return paths_list