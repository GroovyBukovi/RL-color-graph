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

    def reset(self, max_new_edges_ratio=0.5):
        self.graph = nx.Graph()
        self.colors = {1 : 'Gray', 2: 'Gray', 3: 'Gray', 4: 'Gray'}  # Store node colors
        self.max_new_edges_ratio = max_new_edges_ratio
        # Define the exact initial graph structure
        initial_edges = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]

        # Add nodes and edges to the graph
        for edge in initial_edges:
            self.graph.add_edge(*edge)

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
        #new_node = max(self.graph.nodes) + 1 if self.graph.nodes else 1
        new_node = len(self.graph.nodes) + 1
        self.graph.add_node(new_node)
        self.colors.setdefault(new_node, "Gray")

        existing_nodes = list(self.graph.nodes)
        existing_nodes.remove(new_node)
        total_existing_edges = self.graph.number_of_edges()

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

    def removeNode(self, node):
        """Removes a node from the graph along with all its edges."""
        if node in self.graph.nodes:
            self.graph.remove_node(node)  # Remove node and its edges from NetworkX graph
            self.colors.pop(node, None)  # Remove node color from tracking
            print(f"Node {node} and its edges have been removed.")
        else:
            print(f"Node {node} does not exist in the graph.")

    def colorNode(self, node, color):
        """Assigns a color to a node if it is not already colored."""
        self.colors[node] = color

    def getNodeColor(self, node):
        """Returns the color of a specific node."""
        return self.colors.get(node, "Node not found")

    def findNeighboringConflicts(self):
        """Finds and prints neighboring nodes that have the same color. If none exist, prints success message."""
        conflicts_found = False  # Track if any conflicts exist

        for node in self.graph.nodes:
            node_color = self.colors.get(node, "Gray")  # Get current node's color
            for neighbor in self.graph.neighbors(node):
                neighbor_color = self.colors.get(neighbor, "Gray")

                if node_color == neighbor_color:  # If colors are the same, it's a conflict
                    print(f" Conflict: Node {node} and Node {neighbor} both have color {node_color}.")
                    conflicts_found = True

        if not conflicts_found:
            print(" No conflicts found. All neighboring nodes have different colors.")

    def visualize(self, name):
        """Draws the graph using networkx and matplotlib."""
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.graph)  # Layout for visualization

        node_colors = [self.colors.get(node, 'gray') for node in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, edge_color='black', node_size=450,
                font_size=15, font_color='white')

        plt.savefig(name)  # Save instead of show
        print("Graph visualization saved")


    def printEdges(self):
        """Prints the current state of connections as a list of tuples."""
        print(list(self.graph.edges))

