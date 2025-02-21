from graph import Graph
from agent import Agent

class Environment:

    def __init__(self,number_of_agents, colors, reward, penalty):
        """
        Initialize the graph with the exact structure described in the exercise.
        """
        agent_counter = 1
        self.graph = Graph()
        self.reward = reward
        self.penalty =penalty
        self.agents = []
        self.colors = colors
        for i in range (number_of_agents):
            new_agent = Agent(agent_counter,self)
            self.agents.append(new_agent)
            agent_counter = agent_counter + 1



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

    def getCurrentState(self):
        return self.graph, self.graph.getNodeColor()

    def agentAction(self, agent, node, color):
        if self.graph.getNodeColor(node) == 'Gray':
            self.graph.colorNode(node,color)
            print("Neighbours : ", self.graph.getNeighborsColors(node))
            if color in self.graph.getNeighborsColors(node):
                print("Wrong coloring")
            else:
                agent.getAndStoreReward(1)
            print(agent.score)
        else:
            print("Already colored node")
            agent.getAndStoreReward(-1)
            print(agent.score)
