import json
import os
from matplotlib import pyplot as plt

for filename in os.listdir('trajectories'):
    with open('trajectories/' + filename, encoding='utf8') as f:
        trajectories = json.load(f)
        for trajectory in trajectories:
            plot = [trajectory['pos'][key] for key in trajectory['pos']]
            plt.plot(plot)

        plt.show()