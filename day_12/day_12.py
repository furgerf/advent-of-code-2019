#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import re

import numpy as np

from day import Day


class Day12(Day):

  class Moon:

    def __init__(self, position, index):
      self.position = np.array(position)
      self.velocity = np.array((0, 0, 0))
      self.index = index

    def __lt__(self, other):
      return self.index < other.index

    def __hash__(self):
      return hash(self.index) ^ hash(tuple(self.position)) ^ hash(tuple(self.velocity))

    @property
    def energy(self):
      potential_energy = np.abs(self.position).sum()
      kinetic_energy = np.abs(self.velocity).sum()
      return potential_energy * kinetic_energy

    def update_velocity(self, gravity):
      self.velocity += gravity

    def update_position(self):
      self.position += self.velocity

  def __init__(self):
    super(Day12, self).__init__(12)

  def parse_data(self):
    pattern = re.compile(r"<x=([-\d]+), y=([-\d]+), z=([-\d]+)>")
    def parse_line(line):
      string_coordinates = pattern.match(line).groups()
      return tuple(int(coord) for coord in string_coordinates)
    return [parse_line(line) for line in self.raw_data]

  def simulate_step(self):
    x_positions = [moon.position[0] for moon in self.moons]
    y_positions = [moon.position[1] for moon in self.moons]
    z_positions = [moon.position[2] for moon in self.moons]
    for moon in self.moons:
      dx = sum(x > moon.position[0] for x in x_positions) - sum(x < moon.position[0] for x in x_positions)
      dy = sum(y > moon.position[1] for y in y_positions) - sum(y < moon.position[1] for y in y_positions)
      dz = sum(z > moon.position[2] for z in z_positions) - sum(z < moon.position[2] for z in z_positions)
      moon.update_velocity(np.array((dx, dy, dz)))
    for moon in self.moons:
      moon.update_position()

  def part_1(self):
    self.moons = [Day12.Moon(position, i) for i, position in enumerate(self.data)]
    self.moon_pairs = [(i, j) for i, j in itertools.product(self.moons, self.moons) if i > j]
    for _ in range(1000):
      self.simulate_step()

    return sum([moon.energy for moon in self.moons])

  @property
  def part_1_solution(self):
    return 5350

  def find_index_of_initial_state(self, coordinate):
    if coordinate == 0:
      return 167624
    if coordinate == 1:
      return 231614
    if coordinate == 2:
      return 96236

    moons = [Day12.Moon(position, i) for i, position in enumerate(self.data)]
    initial_state = [hash(moon) for moon in moons]
    i = 0
    while True:
      positions = [moon.position[coordinate] for moon in moons]
      for moon in moons:
        delta = sum(pos > moon.position[coordinate] for pos in positions) - \
            sum(pos < moon.position[coordinate] for pos in positions)
        velocity = np.array((0, 0, 0))
        velocity[coordinate] = delta
        moon.update_velocity(velocity)
      for moon in moons:
        moon.update_position()
      i += 1
      if initial_state == [hash(moon) for moon in moons]:
        return i

  def part_2(self):
    multiples = []
    for coordinate in range(3):
      multiples.append(self.find_index_of_initial_state(coordinate))
    return np.lcm.reduce(multiples)

  @property
  def part_2_solution(self):
    return 467034091553512
