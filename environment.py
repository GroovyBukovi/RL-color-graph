from graph import Graph
from agent import Agent
from QLearningAgent import QLearningAgent

class Environment:

    def __init__(self,number_of_agents, colors, reward, penalty, k):
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
        '''for i in range (number_of_agents):
            new_agent = QLearningAgent(agent_counter, self)
            self.agents.append(new_agent)
            agent_counter = agent_counter + 1'''
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


    def getCurrentState(self):
        """Returns a tuple representing the current state of the graph."""
        node_colors = tuple(self.graph.colors.values())  # Color of each node
        adjacency_matrix = tuple(
            tuple(1 if j in self.graph.getNeighbors(i) else 0 for j in self.graph.getNodes()) for i in
            self.graph.getNodes())

        return (node_colors, adjacency_matrix)  # Return state tuple

