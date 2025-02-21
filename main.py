from environment import Environment

e = Environment(4, ['cyan', 'magenta', 'brown', 'pink', 'olive', 'gold', 'red', 'blue', 'green', 'purple', 'orange'], 1, -1)

print(e.graph.getNodes())




for i in range(7):
    print("K=", i)
    for i in e.getAgents():
        i.attemptToColorNode(i.selectNode(), i.selectColor())
    e.advanceToNextState()




e.graph.visualize()
