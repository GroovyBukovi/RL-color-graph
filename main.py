import random
from environment import Environment
from QLearningAgent import QLearningAgent


e = Environment(['cyan', 'brown', 'pink', 'olive', 'gold', 'red', 'blue', 'green', 'orange', 'violet'], 5, -1, 6)
print(e.graph.getNodes())
print(e.graph.colors.values())
#print(e.graphIsColored())


e.agent.train(1)
e.graph.visualize('graph10.png')
print(e.agent.saveQTableToCsv())




