import random
import numpy as np
from agent import Agent
import matplotlib.pyplot as plt


class QLearningAgent(Agent):
    def __init__(self, agent_id, environment, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.2, min_epsilon=0.1):
        super().__init__(agent_id, environment)
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration probability
        self.epsilon_decay = epsilon_decay  # Decay rate of epsilon
        self.min_epsilon = min_epsilon  # Minimum value for epsilon
        self.q_table = {}  # Q-value table
        self.episode_scores = []

    def get_q_value(self, state, action):
        print("GET", self.q_table.get(state, action))
        return self.q_table.get((state, action), 0.0)


    def update_q_value(self, state, action, reward, next_state):
        max_q_next = max([self.get_q_value(next_state, a) for a in self.get_possible_actions(next_state)], default=0.0)
        current_q = self.get_q_value(state, action)
        # bellman equation
        new_q = current_q + self.alpha * (reward + self.gamma * max_q_next - current_q)
        print("NEW Q: ", new_q)
        self.q_table[(state, action)] = new_q



    def get_possible_actions(self, state):
        nodes = self.environment.getGraph().getNodes()
        colors = self.environment.getColors()

        actions = [(node, color) for node in nodes for color in colors]
        return actions

    def select_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if random.random() < self.epsilon:  # Exploration
            return random.choice(possible_actions)
        else:  # Exploitation
            q_values = {action: self.get_q_value(state, action) for action in possible_actions}
            best_action = max(q_values, key=q_values.get)  # Action with max Q-value
            best_q_value = q_values[best_action]  # Get its Q-value

            print("Best Action:", best_action, "| Q-value:", best_q_value)  # Print both
            return best_action

    '''def select_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if random.random() < self.epsilon:  # Exploration
            action = random.choice(possible_actions)
        else:  # Exploitation
            q_values = {action: self.get_q_value(state, action) for action in possible_actions}
            action = max(q_values, key=q_values.get)

        return action, self.get_q_value(state, action)  # Now it returns the Q-value too'''

    def train(self, episodes):
        steps_per_episode = self.environment.k

        for episode in range(1, episodes + 1):
            print("Episode ", episode)
            self.environment.getGraph().reset()  # Reset environment
            episode_score = 0  # Reset total score for the episode

            for step in range(0, steps_per_episode + 1):
                print("Step is ", step)

                print("Total nodes ", len(self.environment.graph.getNodes()))
                while not self.environment.graphIsColored():
                    state = self.environment.getCurrentState()  # Get current state
                    action = self.select_action(state)  # Select action

                    node, color = action
                    self.attemptToColorNode(node, color)  # Perform action
                    reward = self.reward_memory[-1]  # Get latest reward

                    episode_score += reward  # Accumulate episode reward
                    next_state = self.environment.getCurrentState()  # Get new state
                    self.update_q_value(state, action, reward, next_state)  # Update Q-table
                    #print("Q TABLE: ", self.q_table)
            nodes = self.environment.graph.getNodes()
            if len(nodes) > 0:
                last_node = max(nodes)  # Get the highest-numbered node (assumed last added)
                self.environment.graph.removeNode(last_node)  # Remove the last node
                print(f"Removed last node: {last_node}")

            self.episode_scores.append(episode_score)  # Store total score for the episode
            #print("Episode scores: ", self.episode_scores)
            # Decay epsilon
            self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)
            #print(f"Q-table at the end of episode {episode}: {self.q_table}")
        print("Training complete.")


        plt.figure(figsize=(40, 24))
        plt.plot(range(1, len(self.episode_scores) + 1), self.episode_scores, marker='o', linestyle='-', color='b')

        plt.xlabel("Episode")
        plt.ylabel("Cumulative Reward")
        plt.title("Agent's Cumulative Rewards Over Episodes")
        plt.grid(True)
        plt.savefig("plot")  # Save the figure
        print(f"Plot saved as plot")

