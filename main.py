
from environment import Environment
from QLearningAgent import QLearningAgent


e = Environment(1, ['black', 'cyan', 'maroon', 'brown', 'pink', 'olive', 'gold', 'red', 'blue',
                    'green', 'purple', 'orange', 'lime', 'violet'], 1, -1, 6)
print(e.graph.getNodes())
print(e.graph.colors.values())
#print(e.graphIsColored())



'''for i in range(7):
    print("K=", i)
    for i in e.getAgents():
        for j in range(1,len(e.graph.getNodes())):
            i.attemptToColorNode(i.selectNode(), i.selectColor())
    e.advanceToNextState()'''

'''episodes = 0
while episodes < 6:
    episodes = episodes + 1
    print("Episode number ", episodes)
    while e.k <=6:
        print(e.agent.get_possible_actions())
        print("K now is ", e.k)
        e.graphIsColored()
        print("Number of nodes is ", len(e.graph.getNodes()))
        for i in e.getAgents():
            for node in e.graph.getNodes():
                i.attemptToColorNode(node, i.selectColor())
    e.graph.visualize()
    e.endEpisode()'''

e.agent.train(1000)
e.graph.visualize('graph10.png')




