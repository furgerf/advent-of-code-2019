#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from day import Day


class Day10(Day):

  def __init__(self):
    super(Day10, self).__init__(10)

  def parse_data(self):
    asteroids = [[position == "#" for position in line] for line in self.raw_data]
    return np.array(asteroids).T

  def detect_asteroids(self, own_coordinates):
    detected_asteroids = {}
    for index, is_asteroid in np.ndenumerate(self.data):
      if not is_asteroid or index == own_coordinates:
        continue

      dx = index[0] - own_coordinates[0]
      dy = -(index[1] - own_coordinates[1])
      angle = np.mod(360 + np.rad2deg(np.arctan2(dx, dy)), 360)
      if angle not in detected_asteroids:
        detected_asteroids[angle] = []
      detected_asteroids[angle].append(index)

    for key, value in detected_asteroids.items():
      detected_asteroids[key] = list(sorted(value, key=lambda item:
          abs(item[0] - own_coordinates[0]) + abs(item[1] - own_coordinates[1])))

    return detected_asteroids

  def part_1(self):
    max_asteroids = 0
    for index, is_asteroid in np.ndenumerate(self.data):
      if not is_asteroid:
        continue

      spotted_asteroids = len(self.detect_asteroids(index))
      max_asteroids = max(max_asteroids, spotted_asteroids)

    return max_asteroids

  @property
  def part_1_solution(self):
    return 334

  def part_2(self):
    station = (23, 20)
    vaporized = 0
    detected_asteroids = self.detect_asteroids(station)

    while sum([len(indices) for indices in detected_asteroids.values()]):
      for angle in sorted(detected_asteroids):
        coordinate = detected_asteroids[angle].pop(0)
        vaporized += 1
        if vaporized == 200:
          return coordinate[0] * 100 + coordinate[1]

  @property
  def part_2_solution(self):
    return 1119
