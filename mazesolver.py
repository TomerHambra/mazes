import pygame as pg
from random import random
from collections import deque
import numpy as np
import gen

def check_events():
  global reset, csv, grid, cols, rows, alg_it, algos, width, height, graph
  for event in pg.event.get():
    if event.type == pg.QUIT: exit()
    if event.type == pg.KEYUP:
      if event.key == pg.K_SPACE: reset = True
      if event.key == pg.K_r: setup(), solve()
      if event.key == pg.K_LEFT:
        alg_it = (alg_it + 1) % len(algos)
        reset = True
      if event.key == pg.K_RIGHT:
        n = len(algos)
        alg_it = ((alg_it - 1) % n + n) % n
        reset = True

def get_rect(x, y):
  return x * TILE, y * TILE, TILE, TILE
def get_next_nodes(x, y):
  check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
  ways = [-1, 0], [0, -1], [1, 0], [0, 1]
  return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]
def get_click_mouse_pos():
  x, y = pg.mouse.get_pos()
  grid_x, grid_y = x // TILE, y // TILE
  pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
  click = pg.mouse.get_pressed()
  return (grid_x, grid_y) if click[0] else False

def dfs(start, goal, graph):
  stack = [start]
  while stack:
    cur_node = stack.pop()
    pg.draw.rect(sc, pg.Color('skyblue3'), get_rect(*cur_node), TILE)
    pg.event.get()
    pg.display.flip()
    if cur_node == goal:
      return stack, visited
    next_nodes = graph[cur_node]
    for next_node in next_nodes:
      if next_node not in visited:
        stack.append(next_node)
        visited[next_node] = cur_node
  return True
        
def bfs(start, goal, graph):
  queue = deque([start])
  while queue:
    cur_node = queue.popleft()
    pg.draw.rect(sc, pg.Color('skyblue3'), get_rect(*cur_node), TILE)
    pg.event.get()
    pg.display.flip()
    if cur_node == goal:
      return queue, visited
    next_nodes = graph[cur_node]
    for next_node in next_nodes:
      if next_node not in visited:
        queue.append(next_node)
        visited[next_node] = cur_node
  return True

def setup():
  global algos, alg_it, width, height, csv, grid, cols, rows, sc, clock, graph, start, queue, visited, reset, TILE, RESW, RESH, algo_names
  algos = [bfs, dfs]
  algo_names = ['Breadth - First Search', 'Depth - First Search']
  width, height = 300, 300
  gen.make_maze(width, height, '0')
  csv = open('maze0.csv', 'r')
  grid = np.loadtxt(csv, delimiter=',').astype(int).tolist()
  cols, rows = len(grid[0]), len(grid)
  RESH, RESW = 1900, 1060
  TILE = max(min(RESH, RESW) // (width), 1)
  pg.init()
  sc = pg.display.set_mode([RESH, RESW])
  clock = pg.time.Clock()
  graph = {}
  for y, row in enumerate(grid):
    for x, col in enumerate(row):
      if not col:
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)
  start = (1, 0)
  queue = deque([start])
  visited = {start: None}
  clock.tick(144)
  reset = True

def solve():
  global reset, queue, visited, algos, goal
  sc.fill(pg.Color('white'))
  [[pg.draw.rect(sc, pg.Color('black'), get_rect(x, y)) for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
  [pg.draw.rect(sc, pg.Color('grey33'), get_rect(x, y)) for x, y in visited]
  [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]
  # mouse_pos = get_click_mouse_pos()
  font = pg.font.Font('freesansbold.ttf', 48)
  text = font.render(algo_names[alg_it], True, (0, 0, 0), (255, 255, 255))
  textRect = text.get_rect()
  textRect.topright = (RESH, 0)
  sc.blit(text, textRect)

  goal = (len(grid)-2,len(grid[0])-1)
  pg.draw.rect(sc, pg.Color('lightblue'), get_rect(*goal), TILE)

  queue = deque([start])
  visited = {start: None}
  algos[alg_it](start, goal, graph)

  path_head, path_segment = goal, goal
  while path_segment and path_segment in visited:
    pg.draw.rect(sc, pg.Color('green3'), get_rect(*path_segment), TILE)
    path_segment = visited[path_segment]
    check_events()
    pg.display.flip()

  pg.draw.rect(sc, pg.Color('crimson'), get_rect(*start), TILE)
  pg.draw.rect(sc, pg.Color('lightblue'), get_rect(*path_head), TILE) 
  check_events()
  pg.display.flip()
  reset = False
  
def main():
  global alg_it, reset
  alg_it = 1
  pg.display.set_caption('Maze')
  setup()
  while True:
    if reset: solve()
    check_events()
    pg.display.update()
    pg.display.flip()
    clock.tick(144)
    
main()