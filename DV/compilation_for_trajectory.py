import csv
import os
import json
import numpy as np
from math import cos, sin
from matplotlib import pyplot as plt


unit = 0.005
l_unit = 0.02
min_lat = 39.2
min_lng = 115.5

for filename in os.listdir('trajectories'):
    output = []
    with open('trajectories/' + filename, encoding='utf8') as f:
        trajectories = json.load(f)
        for trajectory in trajectories:
            positions = trajectory['pos']
            new_positions = {}
            not_dictionary = []
            for time in positions:
                not_dictionary.append((positions[time][0] * unit + min_lat, positions[time][1] * unit + min_lng))
                new_positions[time] = not_dictionary[-1]
            x = np.array([not_dictionary[-1][0] - not_dictionary[0][0], not_dictionary[-1][1] - not_dictionary[0][1]])
            try:
                x = x / np.linalg.norm(x)
            except:
                raise Exception(x)
            o = np.array(not_dictionary[0])
            theta = np.arccos(np.clip(np.dot(x, np.array([1, 0])), -1.0, 1.0))
            rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
            for_display = []
            for item in not_dictionary:
                for_display.append(np.dot(rot, (np.array(item) - o)).tolist())
            count = 0
            for time in new_positions:
                for_display[count][0] = int(time)
                count += 1
            trajectory['pos'] = new_positions
            trajectory['display'] = for_display

    with open('trajectories/' + filename, mode='w', encoding='utf8') as f:
        json.dump(trajectories, f)
