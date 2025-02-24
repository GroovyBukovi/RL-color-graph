import random
import pandas as pd
import csv
from agent import Agent
import matplotlib.pyplot as plt


class QLearningAgent(Agent):
    def __init__(self, agent_id, environment, alpha=0.3, gamma=0.8, epsilon=1.0, epsilon_decay=0.0001, min_epsilon=0.15, bias= 0.1):
        super().__init__(agent_id, environment)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability
        self.epsilon_decay = epsilon_decay  # Decay rate of epsilon
        self.min_epsilon = min_epsilon
        self.bias = bias# Minimum value for epsilon
        self.q_table = {}  # Q-value table
        self.episode_scores = []


    def getQValue(self, state, action):
        return self.q_table.get((state, action), self.bias)

    def updateQValue(self, state, action, reward, next_state):
        if (state, action) not in self.q_table:
            self.q_table[(state, action)] = self.bias  # Small positive bias for stability

        possible_actions = self.getPossibleActions(next_state)
        max_q_next = max([self.getQValue(next_state, a) for a in possible_actions], default=self.bias)

        current_q = self.getQValue(state, action)

        # Modify penalty weight to prevent over-negative bias
        adjusted_reward = reward if reward > 0 else reward * 0.5 # Reduce impact of penalties

        new_q = current_q + self.alpha * (adjusted_reward + (self.gamma * max_q_next) - current_q)

        self.q_table[(state, action)] = new_q

    def getPossibleActions(self, state):
        nodes = self.environment.getGraph().getNodes()
        colors = self.environment.getColors()

        actions = [(node, color) for node in nodes for color in colors]
        return actions

    def selectAction(self, state):
        possible_actions = self.getPossibleActions(state)

        if random.random() < self.epsilon:  # Exploration
            return random.choice(possible_actions)
        else:  # Exploitation
            q_values = {action: self.getQValue(state, action) for action in possible_actions}
            for action, q_value in q_values.items():
                print(f"   Action: {action} → Q-value: {q_value}")
            best_action = max(q_values, key=q_values.get)  # Action with max Q-value
            best_q_value = q_values[best_action]  # Get its Q-value

            print("Best Action:", best_action, "| Q-value:", best_q_value)  # Print both
            return best_action


    def train(self, episodes):
        steps_per_episode = self.environment.k
        df_epsilon = pd.DataFrame(columns=["Episode", "Epsilon"])
        df_correctly_colored = pd.DataFrame(columns=["Episode", "correctly colored"])

        for episode in range(1, episodes + 1):
            self.environment.getGraph().reset()
            episode_score = 0

            for step in range(steps_per_episode +1):
                while not self.environment.graphIsColored():
                    node = random.choice(self.environment.getGraph().getNodes())
                    state = self.environment.getCurrentState(action_node=node)
                    action = self.selectAction(state)
                    node, color = action
                    self.attemptToColorNode(node, color)

                    reward = self.reward_memory[-1] if self.reward_memory else 0
                    episode_score += reward

                    next_state = self.environment.getCurrentState(action_node=node)
                    self.updateQValue(state, action, reward, next_state)
                # count correctly colored nodes
                if len(self.environment.getGraph().getNodes()) == 10:
                    correct_nodes = self.environment.count_correctly_colored_nodes()
                    print(f"Correctly colored nodes (when nodes=10): {correct_nodes}")

            new_row = pd.DataFrame({"Episode": [episode], "Correctly Colored": [correct_nodes]})
            df_correctly_colored = pd.concat([df_correctly_colored, new_row], ignore_index=True)

            self.episode_scores.append(episode_score)
            self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)
            nodes = self.environment.graph.getNodes()

            if len(nodes) > 0:
                last_node = max(nodes)  # Get the highest-numbered node (assumed last added)
                self.environment.graph.removeNode(last_node)  # Remove the last node
                print(f"Removed last node: {last_node}")
                # Decay epsilon

            new_row = pd.DataFrame({"Episode": [episode], "Epsilon": [self.epsilon]})
            df_epsilon = pd.concat([df_epsilon, new_row], ignore_index=True)
            self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)

        csv_filename = "epsilon_decay.csv"
        df_epsilon.to_csv(csv_filename, index=False)

        csv_filename = "correctly_colored.csv"
        df_correctly_colored.to_csv(csv_filename, index=False)

        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(self.episode_scores) + 1), self.episode_scores, marker='o', linestyle='-', color='b')
        plt.xlabel("Episode")
        plt.ylabel("Cumulative Reward")
        plt.title("Agent's Cumulative Rewards Over Episodes")
        plt.grid(True)
        plt.savefig("plot")


    def saveQTableToCsv(self, filename="q_table.csv"):
        if not self.q_table:
            print("Warning: Q-table is empty. Nothing to save.")
            return

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Node Colors", "Adjacency Info", "Action", "Q-value"])
            for (state, action), q_value in self.q_table.items():
                writer.writerow([state[0], state[1], action, q_value])
        print(f"Q-table saved to {filename}")