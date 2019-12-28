#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day

class Day06(Day):

  def __init__(self):
    super(Day06, self).__init__(6)

  def parse_data(self):
    return [(line[:line.index(")")], line[line.index(")")+1:]) for line in self.raw_data]

  def part_1(self):
    direct_orbits = {}

    for source, destination in self.data:
      if source not in direct_orbits:
        direct_orbits[source] = []
      direct_orbits[source].append(destination)

    def count_orbits(source):
      if source not in direct_orbits:
        return 0, 1
      count = 0
      all_children = 0
      for destination in direct_orbits[source]:
        sub_total, children = count_orbits(destination)
        count += sub_total
        all_children += children
      return count + all_children, all_children + 1

    origin = "COM"

    def other_count_orbits(source, depth):
      if source not in direct_orbits:
        return 0
      return depth * len(direct_orbits[source]) + \
          sum([other_count_orbits(destination, depth+1) for destination in direct_orbits[source]])
    return other_count_orbits(origin, 1)

  @property
  def part_1_solution(self):
    return 130681

  def part_2(self):
    reverse_orbits = {}
    for source, destination in self.data:
      reverse_orbits[destination] = source

    def find_paths(source, path):
      if source not in reverse_orbits:
        return path
      return find_paths(reverse_orbits[source], [reverse_orbits[source]] + path)

    my_path = find_paths("YOU", [])
    santa_path = find_paths("SAN", [])

    for i in range(min(len(my_path), len(santa_path))):
      if my_path[i] != santa_path[i]:
        return len(my_path[i:]) + len(santa_path[i:])
    return None

  @property
  def part_2_solution(self):
    return 313
