import matplotlib.pyplot as plt
from IPython import display

plt.ion()
plt.show(block=False)

def plot_scores(scores, mean_scores):
    plt.figure(1)
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Score vs. Number of Games')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.pause(.1)

def plot_reward(game_nums,rewards):
    plt.figure(2)
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.plot(game_nums, rewards, marker='o', linestyle='-', color='b')
    plt.title('Reward vs. Number of Games')
    plt.xlabel('Number of Games')
    plt.ylabel('Reward')
    plt.grid(True)
    plt.tight_layout()
