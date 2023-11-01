import csv
import os
import random
import json

import numpy as np
from matplotlib import pyplot as plt

unit = 0.005  # 400 * 400 in lat&lng
map_grid_size = 400
radius = 0.02  # 100 * 100, in lat&lng
radius_squared = radius * radius
hash_grid_size = 100
grid_extension = 2
units_in_grid = int(map_grid_size / hash_grid_size)

min_lat = 39.2
min_lng = 115.5
l_unit = 2.0 / hash_grid_size  # essentially same as radius

phone_bonus = 4
proximity_bonus = 5.3
category_bonus = 1

# init height map
map_grid = np.zeros((map_grid_size, map_grid_size), dtype=float)
# init for other things
hash_grid = [[[[] for k in range(hash_grid_size + 4)] for j in range(hash_grid_size + 4)] for i in range(288)]
trajectory_list = []
trajectories = [[] for i in range(288)]
trajectory_radius = 0.08  # in lat&lng
trajectory_radius_squared = trajectory_radius * trajectory_radius

timeout_time = 4
min_threshold = 20


def CalcGrid(time, current_trajectory, last_location=None):
    current_max = min_threshold
    max_list = []
    grid = hash_grid[time]
    for y_grid in range(grid_extension, hash_grid_size + grid_extension + 1):
        for x_grid in range(grid_extension, hash_grid_size + grid_extension + 1):
            if update_grid[time][y_grid][x_grid]:
                for y in range(y_grid * units_in_grid, (y_grid + 1) * units_in_grid):
                    for x in range(x_grid * units_in_grid, (x_grid + 1) * units_in_grid):
                        lat = y * unit
                        lng = x * unit

                        value = 0
                        local_grid = []
                        for i in range(y_grid, y_grid + grid_extension * 2 + 1):
                            for j in range(x_grid, x_grid + grid_extension * 2 + 1):
                                try:
                                    local_grid += grid[i][j]
                                except:
                                    pass
                        for data in local_grid:
                            dx = float(data['lat']) - min_lat - lat
                            dy = float(data['lng']) - min_lng - lng

                            if dx * dx + dy * dy <= radius_squared:
                                value += 1 + random.random() * 0.01
                                if current_trajectory is not None:
                                    if data['phone'] in trajectory_list[current_trajectory]['phones']:
                                        value += phone_bonus
                                    if int(data['label']) == trajectory_list[current_trajectory]['max_label']:
                                        value += category_bonus

                        if last_location:
                            dx = last_location[0] - lat
                            dy = last_location[1] - lng
                            if dx * dx + dy * dy <= trajectory_radius_squared:
                                value *= proximity_bonus

                        try:
                            map_grid[y][x] = value
                        except:
                            pass
                        if value > current_max:
                            current_max = value
                            max_list = [(y, x)]
                        elif value == current_max:
                            max_list.append((y, x))

    retval = [0, 0]
    if len(max_list) == 1:
        return max_list[0]
    elif len(max_list) == 0:
        return None
    else:
        for item in max_list:
            retval[0] += item[0]
            retval[1] += item[1]
        retval[0] /= len(max_list)
        retval[1] /= len(max_list)
    return retval


for filename in os.listdir('processed_data'):
    # init hash grid
    hash_grid = [[[[] for k in range(hash_grid_size + grid_extension * 2)]
                  for j in range(hash_grid_size + grid_extension * 2)] for i in range(288)]
    update_grid = np.zeros((288, hash_grid_size + grid_extension * 2, hash_grid_size + grid_extension * 2), dtype=bool)
    trajectory_list = []
    with open('hashes_data/' + filename, encoding='utf8') as f_read:
        print("reading " + filename)
        reader = csv.DictReader(f_read)
        fieldnames = reader.fieldnames
        for line in reader:
            t = int(line['time'])
            y = int((float(line['lat']) - min_lat) / l_unit)
            x = int((float(line['lng']) - min_lng) / l_unit)
            hash_grid[t][y + grid_extension][x + grid_extension].append(line)
            for i in range(y - grid_extension, y + grid_extension * 2 + 1):
                for j in range(x - grid_extension, x + grid_extension * 2 + 1):
                    update_grid[t][i][j] = True
        # loop to find trajectories
        completed = [False for i in range(288)]
        count = 0
        output = []
        while True:
            # new trajectory
            print("finding trajectory", count + 1)

            trajectory_list.append({'pos': {}, 'labels': [0, 0, 0, 0, 0], 'time': {}, 'phones': set(), 'max_label': 4})
            last_location = None
            timeout = timeout_time
            flag = False
            for i in range(288):
                if timeout == 0:
                    break
                if completed[i]:
                    if flag:
                        timeout -= 1
                    continue

                print("\rprocessing time", i, end='')
                flag = True
                map_grid = np.zeros((map_grid_size, map_grid_size), dtype=float)
                current_location = CalcGrid(i, count, last_location)
                # plt.imshow(map_grid, cmap='hot')
                # plt.show()
                if current_location is None:
                    timeout -= 1
                    completed[i] = True
                    continue
                if last_location:
                    dy = (current_location[0] - last_location[0]) * unit
                    dx = (current_location[1] - last_location[1]) * unit
                    if dx * dx + dy * dy > trajectory_radius * trajectory_radius:
                        timeout -= 1
                        continue
                timeout = timeout_time
                trajectory_list[-1]['pos'][str(i)] = current_location
                trajectory_list[-1]['time'][str(i)] = [0, 0, 0, 0]
                last_location = current_location

                lat = current_location[0] * unit
                lng = current_location[1] * unit
                y_grid = int(lat / l_unit)
                x_grid = int(lng / l_unit)
                for j in range(y_grid - grid_extension * 2, y_grid + grid_extension * 2 + 1):
                    for k in range(x_grid - grid_extension * 2, x_grid + grid_extension * 2 + 2):
                        current_grid = hash_grid[i][j][k].copy()
                        hash_grid[i][j][k].clear()
                        while len(current_grid):
                            data = current_grid.pop()
                            dx = float(data['lat']) - min_lat - lat
                            dy = float(data['lng']) - min_lng - lng
                            if dx * dx + dy * dy <= trajectory_radius_squared:
                                label = int(data['label'])
                                trajectory_list[-1]['labels'][label] += 1
                                trajectory_list[-1]['time'][str(i)][label] += 1
                                if trajectory_list[-1]['labels'][label] > \
                                        trajectory_list[-1]['labels'][trajectory_list[-1]['max_label']]:
                                    trajectory_list[-1]['max_label'] = label
                                trajectory_list[-1]['phones'].add(data['phone'])
                                temp_output = data.copy()
                                temp_output['trajectory'] = count
                                output.append(temp_output)
                            else:
                                hash_grid[i][j][k].append(data)
            if len(trajectory_list[-1]['pos']) > min_threshold:
                print("\ntrajectory", count + 1, "ended with", len(trajectory_list[-1]['pos']))
                print(trajectory_list[-1]['pos'])
                count += 1
            else:
                print()
                trajectory_list.pop()
            if not flag:
                break
    print("writing", filename)
    with open("trajectory_data/" + filename, mode='w', encoding='utf8', newline='') as f_out:
        out_fieldnames = fieldnames.copy()
        out_fieldnames.append('trajectory')
        writer = csv.DictWriter(f_out, out_fieldnames)
        writer.writeheader()
        writer.writerows(output)

    for trajectory in trajectory_list:
        trajectory['labels'].pop()
        trajectory['phones'] = list(trajectory['phones'])
    with open("trajectories/" + filename[:-4] + '.json', mode='w', encoding='utf8', newline='') as f_out:
        json.dump(trajectory_list, f_out)
