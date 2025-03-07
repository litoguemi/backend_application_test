import networkx as nx
import json
from networkx.algorithms import isomorphism

# ##################################################
# 1) Load workpiece graph and feature graph data from  json file
# ##################################################

# Note: Available files are: workpiece_graph.json, feature_graph.json

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    G = nx.Graph()

    #Adding nodes
    for node in data['nodes']:
        node_id = node[0]
        node_attributes = node[1]
        G.add_node(node_id, **node_attributes)

    #Adding edges
    for edge in data['edges']:
        source = edge[0]
        target = edge[1]
        edge_attributes = edge[2]
        G.add_edge(source, target, **edge_attributes)
    
    return G 

# ##################################################
# 2) Create graphs from loaded data
# ##################################################

# Hint: The library networkx helps you to create a graph. You can use the nx.Graph() class to create a graph.
# Note: Other appraoches are also possible.

workpiece_graph = load_graph_from_json('workpiece_graph.json')
feature_graph = load_graph_from_json('feature_graph.json')

# Note: Optional task - Visualize the graph
# Example code:

from pyvis.network import Network
wnt = Network()
wnt.from_nx(workpiece_graph)
wnt.show("workpiece_graph.html", notebook=False)

fnt = Network()
fnt.from_nx(feature_graph)
fnt.show("feature_graph.html", notebook=False)

# ##################################################
# 3) Check if the feature graph is a subgraph of the workpiece workpiece and find any other matching subgraphs
# ##################################################

def node_match(n1, n2):
    return n1['type'] == n2['type'] and n1['cavity'] == n2['cavity']

def edge_match(e1, e2):
    return e1['angular_type'] == e2['angular_type']

# Checking if the feature graph is a subgraph of the workpiece graph
GM = isomorphism.GraphMatcher(workpiece_graph, feature_graph, node_match=node_match, edge_match=edge_match)

if GM.subgraph_is_isomorphic():
    print("Feature graph is a subgraph of the workpiece graph.")    
else:
    print("The feature graph is not a subgraph of the workpiece graph.")

# ##################################################
# 4) Results
# ##################################################

# Print results if matches are found. Return the number of matches and the node ids.

# Retrieve the matching subgraphs
subgraph_mapping = GM.mapping

num_matches = len(subgraph_mapping)
print(f"Number of matches: {num_matches}")

result = (subgraph_mapping, num_matches)
print("Subgraph mappings: ", result[0])