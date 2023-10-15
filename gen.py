# fuck this file - aj
# Credit: Tomer

import numpy as np
import random, csv


def create_maze(width, height):
  width //= 2
  height //= 2
  maze = np.ones((width * 2 + 1, height * 2 + 1))
  x, y = (0, 0)
  maze[2 * x + 1, 2 * y + 1] = 0
  stack = [(x, y)]
  while len(stack) > 0:
    x, y = stack[-1]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if nx >= 0 and ny >= 0 and nx < width \
          and ny < height and maze[2 * nx + 1, 2 * ny + 1] == 1:
        maze[2 * nx + 1, 2 * ny + 1] = 0
        maze[2 * x + 1 + dx, 2 * y + 1 + dy] = 0
        stack.append((nx, ny))
        break
    else:
      stack.pop()
  maze[1, 0] = 0
  maze[-2, -1] = 0

  return maze


def make_maze(width, height, id):
  maze = create_maze(width, height)
  with open('maze' + id + '.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(list(zip(*maze.astype(int))))