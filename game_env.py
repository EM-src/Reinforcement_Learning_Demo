import pygame
from enum import Enum
from settings import level_map, WIDTH, HEIGHT, BLOCK_SIZE
from collections import namedtuple
import numpy as np


# Pygame setup
pygame.init()


class Direction(Enum):
    INITIAL_POSITION = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


Pos = namedtuple('Pos', 'x,y')


class GameAI:
    def __init__(self):
        # Setup display screen and clock
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        pygame.display.set_caption('PE7046')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.gameReset()
    
    
    def gameReset(self):
        self.move_count = 0
        self.collision_count = 0
        self.level_completed = False
        self.game_over = False
        self.done = False
        self.has_key = False
        self.collision_type = None
        self.game_iteration = 0
        self.score = 0

        # Define game elements and variables
        self.walls, self.key, self.exit, self.player, self.fire = self.gameElements(level_map)
        pygame.draw.rect(self.screen, 'purple', self.player)

        self.Pos = Pos(self.player.x, self.player.y)

        self.direction = Direction.INITIAL_POSITION
        self.drawMap()

    
    # Read the settings file that contains the gamelevel layout and create rectangles for all game elements
    def gameElements(self, layout):
        walls = []
        for x_index, row in enumerate(layout):
            for y_index, col in enumerate(row):
                
                x = y_index * BLOCK_SIZE
                y = x_index * BLOCK_SIZE

                if col == 'X':
                    walls.append(pygame.Rect(x,y, BLOCK_SIZE -1, BLOCK_SIZE -1))
                elif col == 'K':
                    key = pygame.Rect(x,y, BLOCK_SIZE -1, BLOCK_SIZE -1)
                elif col == 'E':
                    exit = pygame.Rect(x,y, BLOCK_SIZE -1, BLOCK_SIZE -1)
                elif col == 'P':
                    player = pygame.Rect(x,y, BLOCK_SIZE -1, BLOCK_SIZE -1)
                elif col == 'F':
                    fire = pygame.Rect(x,y, BLOCK_SIZE -1, BLOCK_SIZE -1)
        return walls, key, exit, player, fire


    # Draw the level placing all previously cretated rectangles in appropriate positions. The player is created in class constructor as
    # it will dynamically chnage its position during the game
    def drawMap(self):
        if self.walls:
            for wall in self.walls:
                pygame.draw.rect(self.screen, 'grey', wall)
        if self.has_key == False:
            pygame.draw.rect(self.screen, 'yellow', self.key)
        pygame.draw.rect(self.screen, 'green', self.exit)
        pygame.draw.rect(self.screen, 'orange', self.fire)


    # Game play step: 
    # 1: Collect agent's input
    # 2: Move the agent
    # 3: Detect collisions and corresponding rewards
    # 4: Update the game UI
    def play_step(self, action):
        self.game_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.move(action)
        self.collisions()
        reward = 0
        if self.collision_type == 'KeyCol':
            reward = 10
        elif self.collision_type == 'ExitCol' and self.has_key:
            reward = 100
        elif self.collision_type == 'ExitCol' and self.has_key == False:
            reward = 0
        elif self.collision_type == 'FireCol':
            reward = -50
        elif self.collision_type == 'WallCol':
            reward = 0
        elif self.collision_type == None:
            reward = 0
        self.collision_type = None
        self.update_UI()

        return reward, self.game_iteration, self.done, self.score
    
  
    # After a player move is done the UI is refreshed:
    # 1: The level map is redrawn 
    # 2: The player is placed in the new position
    # 3: If the game level is completed the final score score is shown
    def update_UI(self):
        self.screen.fill('black')
        self.drawMap()
        pygame.draw.rect(self.screen, 'purple', (self.player.x, self.player.y, BLOCK_SIZE -1, BLOCK_SIZE -1))
        self.clock.tick(60)
        if self.level_completed:
            self.score = self.score_and_game_status()
        pygame.display.flip()
    

    # Move logic for the player. According to user input the blayer will be moving at BLOCK_SIZE steps
    def move(self, action):
        self.move_count += 1
        if np.array_equal(action, [1, 0, 0, 0]):
            self.direction = Direction.LEFT
            self.player.x += BLOCK_SIZE
        elif np.array_equal(action, [0, 1, 0, 0]):
            self.direction = Direction.RIGHT
            self.player.x -= BLOCK_SIZE
        elif np.array_equal(action, [0, 0, 1, 0]):
            self.direction = Direction.DOWN
            self.player.y += BLOCK_SIZE
        elif np.array_equal(action, [0, 0, 0, 1]):
            self.direction = Direction.UP
            self.player.y -= BLOCK_SIZE
        
        self.Pos = Pos(self.player.x, self.player.y)


    # Detection of collisions
    # Walls: If a wall collision is detected the player is drawn into its previous position
    # Key: If a key collision is detected the map is drwan without the key rectangle and the variable has_key is updated to True
    # Exit: If an exit collision is detected and the has _key variable is True then the level is completed
    def collisions(self):
        if self.walls:
            for wall in self.walls:
                if self.player.colliderect(wall):
                    self.collision_type = 'WallCol'
                    self.collision_count += 1
                    # print('wall col:', self.collision_count, self.direction)   # For debugging
                    if self.direction == Direction.LEFT:    # Collison from the left
                        self.move([0, 1, 0, 0]) #Direction.RIGHT)
                    elif self.direction == Direction.RIGHT: # Collision from the right
                        self.move([1, 0, 0, 0]) #Direction.LEFT)
                    elif self.direction == Direction.DOWN:  # Collision from the top
                        self.move([0, 0, 0, 1]) #Direction.UP)
                    elif self.direction == Direction.UP:    # Collision from the bottom
                        self.move([0, 0, 1, 0]) #Direction.DOWN)

        if self.key:
            if self.player.colliderect(self.key):
                self.collision_type = 'KeyCol'
                self.key = None
                self.has_key = True

                # i = 0
                # for j in range(1, 100000000): # Performance Bug
                #     i += j
        
        if self.exit:
            if self.player.colliderect(self.exit):
                self.collision_type = 'ExitCol'
                if self.has_key:
                    self.level_completed = True
                    self.done = True

        if self.fire:
            if self.player.colliderect(self.fire):
                self.collision_type = 'FireCol'
                self.game_over = True
                self.done = True

      
    # Score Count and level completed screen
    def score_and_game_status(self):
        text_font = pygame.font.Font('pixel_font.ttf', 30)
        level_completed_text = 'Door Unlocked!'
        game_over_text = 'Stepped into fire. Game Over...'
        if self.game_over == False:
            valid_moves = self.move_count - 2 * self.collision_count
            level_completed_surf = text_font.render(f'{level_completed_text}', False, 'purple')
            level_completed_rect = level_completed_surf.get_rect(center = (200,150))
            self.screen.fill("Black")
            self.screen.blit(level_completed_surf, level_completed_rect)
            score_message_surf = text_font.render(f'Level completed in {valid_moves} moves...', False, 'purple')
            score_message_rect = score_message_surf.get_rect(center = (200,220))
            self.screen.blit(score_message_surf, score_message_rect)
        else:
            game_over_surf = text_font.render(f'{game_over_text}', False, 'purple')
            game_over_rect = game_over_surf.get_rect(center = (200,200))
            self.screen.fill("Black")
            self.screen.blit(game_over_surf, game_over_rect)
        
        return valid_moves