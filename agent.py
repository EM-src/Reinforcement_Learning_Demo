import random
import torch
from collections import deque
import numpy as np
from game_env import GameAI, Pos
from model import Linear_QNet, QTrainer
from settings import MEM_CAPACITY, BATCH_SIZE, LEARNING_RATE, BLOCK_SIZE
from report import plot_scores, plot_reward
import os

class Agent:
    def __init__(self):
        self.number_of_games = 1
        self.epsilon = 0  # parameter to control the randomness
        self.gamma = 0.9  # discount rate has to be smaller than 1
        self.memory = deque(maxlen = MEM_CAPACITY)  
        self.model = Linear_QNet(5, 256, 4) # 5 inputs (state), 256 hidden layers, 4 outputs (move array)
        if os.path.exists('model/model.pth'):
            self.model.load_state_dict(torch.load('model/model.pth'))
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)

    def get_state(self, game):
        player = game.Pos

        state_array = np.array([
            # Player Pos
            player[0],
            player[1],

            # Key
            int(game.has_key),

            # Fire
            int(game.game_over),

            # Exit
            int(game.level_completed),
        ])

        mask = np.array([1,1,1,1,1]) #  Binary tensor to make sure all elements of state are taken into consideration
        state = state_array * mask
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # Store as one tuple at a time

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            random_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            random_sample = self.memory
        
        state_aggr, action_aggr, reward_aggr, next_state_aggr, done_aggr = zip(*random_sample)
        self.trainer.train_step(state_aggr, action_aggr, reward_aggr, next_state_aggr, done_aggr)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def perform_action(self, state):
        # Random moves: tradeoff between exploration and explotation
        self.epsilon = 400 - self.number_of_games
        move = [0,0,0,0]

        if random.randint(0, 900) < self.epsilon:
            move_idx = random.randint(0,3)
            move[move_idx] = 1
        else:
            state0 = torch.tensor(state, dtype = torch.float)
            prediction = self.model(state0)
            move_idx = torch.argmax(prediction).item()
            move[move_idx] = 1
 
        return move


def train():
    scores = []
    avg_score = []
    rewards = []
    game_nums = []
    total_score = 0
    total_reward = 0
    agent = Agent()
    game = GameAI()

    while True:
        # get the old state
        state_old = agent.get_state(game)

        # get the move
        action = agent.perform_action(state_old)

        # perform the move and get the outputs of the play_step function
        reward, game_iteration, done, score = game.play_step(action)

        # Reward accumulated value
        total_reward += reward

        # get the new state
        state_new = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, action, reward, state_new, done)

        # Add to the experience replay memory
        agent.remember(state_old, action, reward, state_new, done)

        if done:
            # If the game was successfully completed train the model on long memory and save the hyperparameters
            if game.level_completed == True:
                agent.train_long_memory()
                agent.model.save()
                
            # Reset the game if the game is done and increase game episode number. Append the rewards to the total_reward list where
            # each element is the total reward of the episode. Keep track of the scores
            game.gameReset()
            agent.number_of_games += 1
            game_nums.append(agent.number_of_games)
            rewards.append(total_reward)
            scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            avg_score.append(mean_score)

            # Plot the metrics
            plot_scores(scores, avg_score)
            plot_reward(game_nums, rewards)
        
        # If no significant progress is made reset the game
        if game_iteration > 500:
            game.gameReset()
            print("Game has been reset because there was no significant progress")

if __name__ == '__main__':
    train()