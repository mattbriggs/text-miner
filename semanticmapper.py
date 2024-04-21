import networkx as nx
import pandas as pd
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot

# Ensure NLTK WordNet is downloaded
import nltk
nltk.download('wordnet')

# Function to add edges for network map
def add_edges(graph, word):
    synsets = wn.synsets(word)
    for syn in synsets:
        for hyper in syn.hypernyms():
            hyper_name = hyper.name().split('.')[0]
            graph.add_node(hyper_name)  # Add hypernym to graph
            graph.add_edge(word, hyper_name)
        for hypo in syn.hyponyms():
            hypo_name = hypo.name().split('.')[0]
            graph.add_node(hypo_name)  # Add hyponym to graph
            graph.add_edge(word, hypo_name)

# Define your list of terms
terms = ['dog', 'cat', 'mammal', 'tree']

# Create a directed graph
G = nx.DiGraph()

# Add terms and relationships to the graph
for term in terms:
    G.add_node(term)
    add_edges(G, term)

# Output the network map as .viz using Graphviz
write_dot(G, 'semantic_network_map.viz')

# Output relationships to a CSV
edges = pd.DataFrame(list(G.edges), columns=['From', 'To'])
edges.to_csv('network_relationships.csv', index=False)

# Function to draw taxonomy and export to OMPL (a simple XML-like format)
def draw_taxonomy(term, depth=3):
    syn = wn.synsets(term)[0]  # Take the first synset
    hyper = lambda s: s.hypernyms()
    tree = nx.DiGraph(nx.ego_graph(syn, hyper, depth=depth))
    write_dot(tree, f'taxonomy_{term}.viz')  # Saving the taxonomy as a VIZ file
    
    # Simple OMPL-like output for demonstration
    ompl_content = "<items>\n"
    for node in tree:
        label = node.name().split('.')[0]
        ompl_content += f'  <item text="{label}" />\n'
    ompl_content += "</items>\n"
    
    with open(f'taxonomy_{term}.ompl', 'w') as f:
        f.write(ompl_content)

# Generate taxonomy for 'mammal'
draw_taxonomy('mammal')

print("Graph, taxonomy, and CSV have been generated.")
