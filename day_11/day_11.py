#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from day import Day
from imageio import imwrite
from intcode import Intcode


class Day11(Day):

  class PaintingRobot:

    def __init__(self):
      self.position = (0, 0)
      self.orientation = 0
      self.colors = {}

    @property
    def number_of_painted_panels(self):
      return len(self.colors)

    @property
    def create_image(self):
      pixels = self.colors.keys()
      min_x = min([p[0] for p in pixels])
      max_x = max([p[0] for p in pixels])
      min_y = min([p[1] for p in pixels])
      max_y = max([p[1] for p in pixels])
      image = np.zeros(shape=(max_x - min_x + 1, max_y - min_y + 1), dtype=np.uint8)
      for location, color in self.colors.items():
        if color == 1:
          image[location[0] - min_x, location[1] - min_y] = 255
      return image

    def paint(self, color):
      assert color == 0 or color == 1
      self.colors[self.position] = color

    def turn_left(self):
      self.orientation = (self.orientation - 1 + 4) % 4
      return self._move_one()

    def turn_right(self):
      self.orientation = (self.orientation + 1) % 4
      return self._move_one()

    def _move_one(self):
      if self.orientation % 2 == 0:
        self.position = (self.position[0], self.position[1] - self.orientation + 1)
      else:
        self.position = (self.position[0] - self.orientation + 2, self.position[1])
      return self.colors[self.position] if self.position in self.colors else 0 # black

  def __init__(self):
    super(Day11, self).__init__(11)

  def parse_data(self):
    return self.parse_intcode_data()

  def paint_hull(self, initial_color):
    robot = Day11.PaintingRobot()
    intcode = Intcode(self.data[:], inputs=[initial_color])

    while not intcode.partial_compute():
      color = intcode.outputs[-2]
      direction = intcode.outputs[-1]
      robot.paint(color)
      if direction == 0:
        current_color = robot.turn_left()
      else:
        current_color = robot.turn_right()
      intcode.add_input(current_color)

    return robot

  def part_1(self):
    return self.paint_hull(0).number_of_painted_panels

  @property
  def part_1_solution(self):
    return 1863

  def part_2(self):
    image = self.paint_hull(1).create_image
    # imwrite("day_11/image.png", image)
    return image.sum()

  @property
  def part_2_solution(self):
    return 22185
