#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum, unique

import numpy as np

from day import Day
from intcode import Intcode


class Day15(Day):

  @unique
  class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

  @unique
  class Status(Enum):
    WALL = 0
    FLOOR = 1
    OXYGEN = 2

  class MazeFinder:

    ALL_DIRECTIONS = None

    def __init__(self, intcode):
      self.intcode = intcode
      self.position = (0, 0)
      self.path = []
      self.options = {}
      self.walls = set()
      self.floors = set([(0, 0)])
      self.oxygen = set()
      self.min_x = None
      self.min_y = None
      self.map = None
      Day15.MazeFinder.ALL_DIRECTIONS = [Day15.Direction(value) for value in range(1, 5)]

    @property
    def visited_fields(self):
      return self.walls.union(self.floors).union(self.oxygen)

    @staticmethod
    def update_position(position, direction):
      if direction == Day15.Direction.NORTH:
        return (position[0], position[1]+1)
      if direction == Day15.Direction.SOUTH:
        return (position[0], position[1]-1)
      if direction == Day15.Direction.WEST:
        return (position[0]-1, position[1])
      return (position[0]+1, position[1])

    @staticmethod
    def get_direction(source, target):
      dx = source[0] - target[0]
      dy = source[1] - target[1]
      assert (dx == 0) ^ (dy == 0)
      if dx == 0:
        return Day15.Direction.SOUTH if dy > 0 else Day15.Direction.NORTH
      return Day15.Direction.WEST if dx > 0 else Day15.Direction.EAST

    def move(self):
      # add options to move if there aren't any
      if self.position not in self.options:
        target_fields = [(Day15.MazeFinder.update_position(self.position, direction), direction)
            for direction in Day15.MazeFinder.ALL_DIRECTIONS]
        self.options[self.position] = target_fields

      # remove visited target fields
      visited_fields = self.visited_fields
      self.options[self.position] = [pos_dir for pos_dir in self.options[self.position] \
          if not pos_dir[0] in visited_fields]

      if self.options[self.position]:
        # select first of the available directions
        new_position, direction = self.options[self.position][0]
        del self.options[self.position][0]
        self.explore(new_position, direction)
      else:
        # no option available: move back
        if not self.path:
          # nothing else to backtrack, map is completed
          return False

        new_position = self.path[-1]
        direction = Day15.MazeFinder.get_direction(self.position, new_position)
        self.backtrack(new_position, direction)

      return True

    def explore(self, new_position, direction):
      # try to move in the selected direction
      self.intcode.add_input(direction.value)
      self.intcode.partial_compute()
      status = Day15.Status(self.intcode.pop_output())
      if status == Day15.Status.WALL:
        self.walls.add(new_position)
      else:
        self.path.append(self.position)
        self.position = new_position
        if status == Day15.Status.FLOOR:
          self.floors.add(new_position)
        else:
          self.oxygen.add(new_position)

    def backtrack(self, new_position, direction):
      # move back in the selected direction
      self.intcode.add_input(direction.value)
      self.intcode.partial_compute()
      status = Day15.Status(self.intcode.pop_output())
      assert status != Day15.Status.WALL
      del self.path[-1]
      self.position = new_position

    def build_map(self):
      while self.move():
        pass

      self.min_x = min([p[0] for p in self.visited_fields])
      max_x = max([p[0] for p in self.visited_fields])
      self.min_y = min([p[1] for p in self.visited_fields])
      max_y = max([p[1] for p in self.visited_fields])
      self.map = np.zeros(shape=(max_x - self.min_x + 1, max_y - self.min_y + 1), dtype=np.uint8)

      for floor in self.floors:
        self.map[(floor[0]-self.min_x, floor[1]-self.min_y)] = Day15.Status.FLOOR.value
      for wall in self.walls:
        self.map[(wall[0]-self.min_x, wall[1]-self.min_y)] = Day15.Status.WALL.value
      for oxygen in self.oxygen:
        self.map[(oxygen[0]-self.min_x, oxygen[1]-self.min_y)] = Day15.Status.OXYGEN.value

    def print_map(self):
      char_map = {
          0: "?",
          Day15.Status.FLOOR.value: " ",
          Day15.Status.WALL.value: "#",
          Day15.Status.OXYGEN.value: "o"
          }
      for i in range(self.map.shape[0]):
        if i > 0:
          print("")
        for j in range(self.map.shape[1]):
          print(char_map[self.map[i, j]], end="")
      print()

    def find_shortest_path(self, stop_at_origin):
      distances = np.zeros_like(self.map)
      assert len(self.oxygen) == 1
      active_cells = set(self.oxygen)
      distance = 0

      while True:
        distance += 1
        neighbors = set()
        for active_cell in active_cells:
          target_cells = [Day15.MazeFinder.update_position(active_cell, direction)
              for direction in Day15.MazeFinder.ALL_DIRECTIONS]
          floor_cells = [cell for cell in target_cells if \
              self.map[(cell[0]-self.min_x, cell[1]-self.min_y)] == Day15.Status.FLOOR.value and \
              distances[cell] == 0]

          if (0, 0) in floor_cells and stop_at_origin:
            # abort if we've found the origin (and are actually supposed to stop)
            return distance

          for floor_cell in floor_cells:
            distances[floor_cell] = distance
            neighbors.add(floor_cell)

        if not neighbors:
          assert not stop_at_origin, "supposed to find origin before running out of tiles"
          # abort if there are no more cells to find
          # return -1 because the path wasn't extended in this iteration
          return distance - 1
        active_cells = neighbors

  def __init__(self):
    super(Day15, self).__init__(15)

  def parse_data(self):
    return self.parse_intcode_data()

  def part_1(self):
    intcode = Intcode(self.data[:])
    finder = Day15.MazeFinder(intcode)
    finder.build_map()
    # finder.print_map()
    return finder.find_shortest_path(True)

  @property
  def part_1_solution(self):
    return 374

  def part_2(self):
    intcode = Intcode(self.data[:])
    finder = Day15.MazeFinder(intcode)
    finder.build_map()
    return finder.find_shortest_path(False)

  @property
  def part_2_solution(self):
    return 482
