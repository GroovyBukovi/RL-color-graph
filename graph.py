import networkx as nx
import random
import matplotlib.pyplot as plt
from pyvis.network import Network


class Graph:
    def __init__(self, max_new_edges_ratio=0.5):
        """
        Initialize the graph with the exact structure described in the exercise.
        """
        self.graph = nx.Graph()
        self.colors = {1 : 'Gray', 2: 'Gray', 3: 'Gray', 4: 'Gray'}  # Store node colors
        self.max_new_edges_ratio = max_new_edges_ratio
        # Define the exact initial graph structure
        initial_edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]

        # Add nodes and edges to the graph
        for edge in initial_edges:
            self.graph.add_edge(*edge)
#
    def getNodes(self):
        """Returns the list of nodes in the graph."""
        return list(self.graph.nodes)

    def getNeighbors(self, node):
        """Returns a list of neighbors for the given node."""
        if node in self.graph.nodes:
            return list(self.graph.neighbors(node))
        else:
            return "Node not found"

    def getNeighborsColors(self, node):
        """Returns a list of colors for the neighbors of the given node."""
        if node in self.graph.nodes:
            neighbors = self.getNeighbors(node)
            return [self.colors.get(neighbor, "Gray") for neighbor in neighbors]
        else:
            return "Node not found"

    def addNode(self):
        """Adds a new node with random connections, not exceeding 50% of existing edges."""
        print(list(self.graph.nodes))
        new_node = max(self.graph.nodes) + 1 if self.graph.nodes else 1
        self.graph.add_node(new_node)
        self.colors.setdefault(new_node, "Gray")

        existing_nodes = list(self.graph.nodes)
        existing_nodes.remove(new_node)

        total_existing_edges = self.graph.number_of_edges()
        print(total_existing_edges)

        # Determine how many edges the new node should have
        num_edges = random.randint(1 , min(total_existing_edges//2, len(existing_nodes)))
        random_edges = random.sample(existing_nodes, num_edges)

        for node in random_edges:
            self.graph.add_edge(new_node, node)

        new_connections = []
        for node in random_edges:
            self.graph.add_edge(new_node, node)
            new_connections.append((new_node, node))  # Store new connection

        # Print the new connections
        print(f"New node {new_node} added with connections: {new_connections}")

        return new_node

    def colorNode(self, node, color):
        """Assigns a color to a node if it is not already colored."""
        print(node, color)
        self.colors[node] = color

    def getNodeColor(self, node):
        """Returns the color of a specific node."""
        return self.colors.get(node, "Node not found")

    #def isNeighbour(self):


    def visualize(self):
        """Draws the graph using networkx and matplotlib."""
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.graph)  # Layout for visualization

        node_colors = [self.colors.get(node, 'gray') for node in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color='black', node_size=450,
                font_size=15, font_color='white')

        plt.savefig("graph.png")  # Save instead of show
        print("Graph visualization saved as 'graph.png'")


    def printEdges(self):
        """Prints the current state of connections as a list of tuples."""
        print(list(self.graph.edges))

    '''def sortNodes(self):
        for node in self.colors:
            if self.colors[node] is not "Gray":
                self.colored_nodes.append(node)
            else:
                self.uncolored_nodes.append(node)'''




'''# Example Usage
g = Graph()



print(g.get_nodes())
g.print_edges()
for i in range (10):
    new_node = g.add_node()
print(g.get_nodes())
g.print_edges()


for node in g.get_nodes():
    color = random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange'])
    g.color_node(node,color)
g.visualize()
print(g.colors)'''

