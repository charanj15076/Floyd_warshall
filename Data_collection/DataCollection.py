import networkx as nx
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Load the OSM data from an XML file
osm_file = "map_csuf.osm"
tree = ET.parse(osm_file)
root = tree.getroot()

# Create an empty graph
G = nx.Graph()


# Helper function to extract node coordinates
def get_node_coordinates(node):
    lat = float(node.attrib["lat"])
    lon = float(node.attrib["lon"])
    return lat, lon


# Iterate through the XML data to create nodes and edges
for element in root.findall(".//node"):
    node_id = element.attrib["id"]
    lat, lon = get_node_coordinates(element)
    G.add_node(node_id, pos=(lon, lat))  # Add nodes with coordinates

for way in root.findall(".//way"):
    nodes = way.findall(".//nd")
    for i in range(1, len(nodes)):
        node1 = nodes[i - 1].attrib["ref"]
        node2 = nodes[i].attrib["ref"]
        G.add_edge(node1, node2)  # Add edges between nodes

# Example: Find the shortest path between two nodes
# source_node = "122627863"  # Replace with the actual ID of the source node
# target_node = "122627866"  # Replace with the actual ID of the target node
# shortest_path = nx.all_pairs_shortest_path(G, source_node, target_node)

# Print the shortest path
# print("Shortest path:", shortest_path)
source_node = "2679539383"
shortest_paths = nx.single_source_shortest_path_length(G, source_node)
# all_shortest_paths = dict(nx.all_pairs_shortest_path(G))
# Visualize the graph with the shortest path highlighted
# pos = nx.get_node_attributes(G, "pos")
# nx.draw(G, pos, with_labels=False, node_size=5)
# nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color="red", node_size=10)
# nx.draw_networkx_edges(
#     G,
#     pos,
#     edgelist=[
#         (shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)
#     ],
#     edge_color="red",
#     width=2,
# )
shortest_distances = {}
for target_node, distance in shortest_paths.items():
    if source_node != target_node:
        key = f"{source_node}, {target_node}"
        shortest_distances[key] = distance


print(shortest_distances)


# Visualize the graph (optional)
pos = nx.get_node_attributes(G, "pos")
nx.draw(G, pos, with_labels=False, node_size=5)
plt.show()
