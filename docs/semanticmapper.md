pip install nltk networkx matplotlib graphviz pandas

Creating a semantic map in Python from a list of terms using WordNet can be done effectively using libraries such as NLTK for accessing WordNet and NetworkX or Graphviz for visualizing the relationships. You will create two types of visualizations: a network map that shows how terms are interrelated, and an organic taxonomy that displays hierarchical relationships.

Here's a step-by-step guide to achieve this:

### 1. Install Necessary Libraries

First, ensure you have the necessary libraries installed. You can install them using pip:

```bash
pip install nltk networkx matplotlib graphviz
```

You might also need to download the WordNet resource from NLTK:

```python
import nltk
nltk.download('wordnet')
```

### 2. Import Libraries and Load Data

Here's how you can start by importing the necessary libraries and defining your list of terms.

```python
import networkx as nx
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt

# List of terms
terms = ['dog', 'cat', 'mammal', 'tree']
```

### 3. Create a Network Map Using WordNet

You'll need to define relationships between these terms based on their semantic relations in WordNet.

```python
def add_edges(graph, word):
    synsets = wn.synsets(word)
    for syn in synsets:
        for hyper in syn.hypernyms():
            graph.add_node(hyper.name().split('.')[0])  # Add hypernym to graph
            graph.add_edge(word, hyper.name().split('.')[0])
        for hypo in syn.hyponyms():
            graph.add_node(hypo.name().split('.')[0])  # Add hyponym to graph
            graph.add_edge(word, hypo.name().split('.')[0])

# Create a directed graph
G = nx.DiGraph()

# Add terms and relationships to the graph
for term in terms:
    G.add_node(term)
    add_edges(G, term)

# Draw the network map
plt.figure(figsize=(10, 8))
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10, font_weight='bold')
plt.title("Semantic Network Map")
plt.show()
```

### 4. Create an Organic Taxonomy

To create a taxonomy, focus on a single term and explore its hypernyms or hyponyms to build a hierarchical structure.

```python
def draw_taxonomy(term):
    syn = wn.synsets(term)[0]  # Take the first synset
    hyper = lambda s: s.hypernyms()
    tree = nx.DiGraph(nx.ego_graph(syn, hyper, depth=3))
    labels = {node: node.name().split('.')[0] for node in tree.nodes()}
    
    # Draw the taxonomy
    pos = nx.spring_layout(tree, seed=42)
    nx.draw(tree, pos, labels=labels, with_labels=True, node_size=2000, node_color='lightgreen', font_size=8, font_weight='bold')
    plt.title(f"Taxonomy of {term.capitalize()}")
    plt.show()

draw_taxonomy('mammal')
```

### Explanation:

- **Network Map**: This visualization uses WordNet to add both hypernyms (more general terms) and hyponyms (more specific terms) of each term in your list to create a semantic network.
- **Organic Taxonomy**: This focuses on a single term (e.g., 'mammal') and builds a hierarchical structure based on its hypernym relationships. The depth can be adjusted according to how broad or detailed you want the taxonomy to be.

Both visualizations can be adjusted based on the specific requirements of your analysis, such as depth of relationships or specific types of semantic connections (e.g., part-of relationships).


Sure, I'll provide a Python script that performs the following tasks based on your request:

1. **Ingests a list of terms**.
2. **Generates a semantic network graph**, and outputs it as a `.viz` file using Graphviz.
3. **Generates an organic taxonomy** for a specified term and outputs it as `.ompl`.
4. **Exports the relationships as a CSV file**.

### Required Installations

Ensure you have the required packages installed:
```bash
pip install nltk networkx matplotlib graphviz pandas
```
You might also need to install `pygraphviz` for direct Graphviz integration:
```bash
pip install pygraphviz
```

### Python Code

```python
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
```

### Explanation:

1. **Network Map (.viz)**: This script generates a `.viz` file using the `write_dot` function, which you can visualize using Graphviz software or online Graphviz viewers.
2. **Organic Taxonomy (.ompl)**: The script simulates an OMPL (Outline Processor Markup Language) format for demonstration purposes, as true OMPL is more complex and typically XML-based.
3. **CSV Relationships**: It exports the relationships from the graph to a CSV file, listing each edge connection between terms.

This script provides a comprehensive approach to visualizing and documenting the semantic relationships between terms using Python and NLTK's WordNet, along with NetworkX for graph management.