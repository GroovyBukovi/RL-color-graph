from graph import Graph
from agent import Agent
from QLearningAgent import QLearningAgent

class Environment:

    def __init__(self, colors, reward, penalty, k):
        """
        Initialize the graph with the exact structure described in the exercise.
        """
        agent_counter = 1
        self.k=k
        self.graph = Graph()
        self.reward = reward
        self.penalty =penalty
        self.agents = []
        self.colors = colors
        self.agent = QLearningAgent(agent_counter, self)
        #self.agent = Agent(agent_counter, self)



    def getAgents(self):
        return self.agents

    def getGraph(self):
        return self.graph

    def getReward(self):
        return self.reward

    def getPenalty(self):
        return self.penalty

    def advanceToNextState(self):
        self.graph.addNode()

    def getColors(self):
        return self.colors

    def graphIsColored(self):
            if 'Gray' not in self.graph.colors.values():
                self.k = self.k + 1
                self.advanceToNextState()
                return True
            else:
                return False

    def agentAction(self, agent, node, color):
        reward = self.reward
        if self.graph.getNodeColor(node) == 'Gray':
            self.graph.colorNode(node,color)
            if color in self.graph.getNeighborsColors(node):
                agent.getAndStoreReward(0)
            else:
                agent.getAndStoreReward(reward)
        else:
            agent.getAndStoreReward(-1)


    def getCurrentState(self, action_node):
        """Returns a tuple representing the current state for the selected action node."""

        if action_node is None:
            return ("Unknown", ())  # Default state if no node is selected

        # Get the colors of all nodes
        node_colors = tuple(self.graph.colors.values())

        # Get adjacency info only for the action node
        adjacency_info = tuple(1 if neighbor in self.graph.getNeighbors(action_node) else 0
                               for neighbor in self.graph.getNodes())

        return (node_colors, adjacency_info)  # Return only relevant information

    def count_correctly_colored_nodes(self):
        """Counts the number of correctly colored nodes when the graph has exactly 10 nodes."""

        if len(self.graph.getNodes()) != 10:
            return 0  # Only count when the graph has exactly 10 nodes

        correctly_colored_count = 0

        for node in self.graph.getNodes():
            node_color = self.graph.getNodeColor(node)
            if node_color == "Gray":
                continue  # Skip uncolored nodes

            neighbor_colors = self.graph.getNeighborsColors(node)
            if node_color not in neighbor_colors:  # If no neighbors have the same color
                correctly_colored_count += 1

        return correctly_colored_count
