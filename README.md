# Reinforcement_Learning_Demo
 Reinformcement Learning implementation on a 2D game using Pytorch and Pygame frameworks

## Game Description and objective:
 The game is presented in an 8x8 block grid (each block is 50x50 pixels) and the main objective is for the Player (Agent) to first collect a Key then unlock a Door to complete the game level while avoiding  the fire tile that leads to instant game over.
 ### Game Components:
  _The Environment_: It is the game grid with all its game components operating within it, different actions performed by the _Agent_ result in different environments states<br />
  _The Agent_: The purple tile, it can move in black spaces and detects collisions with all other game assets resulting in different environment states<br />
  _The Key_: The yellow tile, once the _Agent_ collides with it it dissapears from the game grid. At this point the _Agent_ is ready to head for the exit<br />
  _The Exit_: The green tile, once the _Agent_ collides with it after having the _Key_ the game level is completed<br />
  _The Fire_: The orange tile, once the _Agent_ collides with it, it is game over<br />

  ![Game elements and level layout](https://github.com/EM-src/Reinforcement_Learning_Demo/assets/105294388/1e2f9cd1-00f2-4586-886b-e0064aebab12)

  ## Optimal Policy
   The Agent in each game iteration has been trained to choose the action which will yield the best results in the optimal policy of the game which is to reach for the Key tile and then head for the level Exit while having performed the least possible amount of moves.<br /> 
   The optimal policy is dictated based on a reward system implemented that awards negative and positive points to the agent for each of its actions based on the state of the environment that they have resulted in. Maximum reward is given for completing the level, a smaller reward is given for collecting the key and negative reward is given for colliding with the fire tile. All other types of collisions do not give any reward.

## The DQN model architecture
The model used for the RL task described in the sections above is DQN. It is a feed forward deep neural nework which takes as an input the current state of environment at a given game iteration and is then connected to 2 hidden layers that in turn are connected to an output layer (with RELU activation) that produces a trensor with 4 values. Based on the maximum of the 4 values the next move is decided.<br />

![DQN model architecture](https://github.com/EM-src/Reinforcement_Learning_Demo/assets/105294388/aa85c8f7-ab32-4c8b-a003-394faa6906f1)

## For reference and comparison a manual game is also provided that needs user input instead of having an automatic agent

