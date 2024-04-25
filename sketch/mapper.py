import networkx as nx
import pandas as pd
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot

# Ensure NLTK WordNet is downloaded
import nltk
nltk.download('wordnet')

def get_terms_from_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the entire content of the file
            content = file.read()
        
        # Split the content by newlines to create a list of terms
        terms_list = content.split('\n')
        
        # Optional: remove any empty strings from the list if blank lines were in the file
        terms_list = [term for term in terms_list if term]
        
        return terms_list
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


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
terms = get_terms_from_file('terms.txt')

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

def draw_taxonomy(term, depth=3):
    import networkx as nx
    from nltk.corpus import wordnet as wn

    # Fetch the synset for the term; assuming 'mammal' is a noun
    syn = wn.synset(f'{term}.n.01')

    # Convert Synset to a string identifier
    syn_id = syn.name()

    # Ensure the graph G is defined and uses string identifiers as nodes
    # This is an example, adjust according to how you actually construct your graph
    G = nx.Graph()
    # Assuming you have a way to add nodes and edges relevant to your taxonomy
    # G.add_node(syn_id)
    # G.add_edge(syn_id, 'other_node_id')

    # Use the corrected node identifier in the ego_graph function
    tree = nx.DiGraph(nx.ego_graph(G, syn_id, radius=depth))

    return tree


# # Function to draw taxonomy and export to OMPL (a simple XML-like format)
# def draw_taxonomy(term, depth=3):
#     syn = wn.synsets(term)[0]  # Take the first synset
#     hyper = lambda s: s.hypernyms()
#     tree = nx.DiGraph(nx.ego_graph(syn, hyper, radius=depth))  # Create a graph of the taxonomy
#     write_dot(tree, f'taxonomy_{term}.viz')  # Saving the taxonomy as a VIZ file
    
#     # Simple OMPL-like output for demonstration
#     ompl_content = "<items>\n"
#     for node in tree:
#         label = node.name().split('.')[0]
#         ompl_content += f'  <item text="{label}" />\n'
#     ompl_content += "</items>\n"
    
#     with open(f'taxonomy_{term}.ompl', 'w') as f:
#         f.write(ompl_content)

# Generate taxonomy for 'mammal'
draw_taxonomy('mammal')

print("Graph, taxonomy, and CSV have been generated.")