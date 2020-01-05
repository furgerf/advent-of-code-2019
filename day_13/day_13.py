#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum, unique

import numpy as np

from day import Day
from intcode import Intcode


class Day13(Day):

  @unique
  class TileType(Enum):
    NOTHING = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

  class GameMap:

    def __init__(self):
      self._game_map = None
      self._paddle_x = None
      self._ball_x = None
      self._current_score = None

    @property
    def paddle_x(self):
      return self._paddle_x

    @property
    def ball_x(self):
      return self._ball_x

    @property
    def current_score(self):
      return self._current_score

    @property
    def number_of_blocks(self):
      return len(np.where(self._game_map == Day13.TileType.BLOCK.value)[0])

    def _initialize_map(self, updates):
      max_x = max(u[0] for u in updates)
      max_y = max(u[1] for u in updates)
      self._game_map = np.zeros(shape=(max_x+1, max_y+1))

    def update_map(self, update_list):
      updates = list(zip(*[update_list[i::3] for i in range(3)]))
      if self._game_map is None:
        self._initialize_map(updates)

      for update in updates:
        if update[0] == -1 and update[1] == 0:
          self._current_score = update[2]
          continue

        self._game_map[update[0], update[1]] = Day13.TileType(update[2]).value
        if update[2] == Day13.TileType.BALL.value:
          self._ball_x = update[0]
        if update[2] == Day13.TileType.PADDLE.value:
          self._paddle_x = update[0]

  def __init__(self):
    super(Day13, self).__init__(13)

  def parse_data(self):
    return self.parse_intcode_data()

  def part_1(self):
    intcode = Intcode(self.data[:])
    intcode.compute()
    game_map = Day13.GameMap()
    game_map.update_map(intcode.outputs)
    return game_map.number_of_blocks

  @property
  def part_1_solution(self):
    return 258

  def part_2(self):
    own_data = self.data[:]
    own_data[0] = 2
    intcode = Intcode(own_data)
    game_map = Day13.GameMap()
    while not intcode.partial_compute():
      game_map.update_map(intcode.outputs)
      intcode.clear_output()
      intcode.add_input(np.sign(game_map.ball_x - game_map.paddle_x))
    game_map.update_map(intcode.outputs)
    return game_map.current_score

  @property
  def part_2_solution(self):
    return 12765
