import random

class Agent:
    def __init__(self, agent_id, environment):
        """Initialize an agent with an ID and reference to the environment."""
        self.agent_id = agent_id
        self.environment = environment
        self.reward_memory = []
        self.score = 0


    def selectNode(self):
        node = random.choice(self.environment.graph.getNodes())
        print("Selected node is: ", node)
        return node

    def selectColor(self):
        color = random.choice(self.environment.getColors())
        print("Selected color is: ", color)
        return color

    def attemptToColorNode(self, node, color):
        """Attempt to color a node and receive a reward."""
        self.environment.agentAction(self, node, color)

    def getAndStoreReward(self, reward):
        """Store the received reward."""
        self.reward_memory.append(reward)
        self.score = self.score + reward

    def displayAgentInfo(self):
        """Print agent statistics."""
        print(f"\nAgent {self.agent_id}:")
        print(f"Total Rewards: {sum(self.reward_memory)}")
