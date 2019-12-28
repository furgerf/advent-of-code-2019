#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day

class Day04(Day):

  def __init__(self):
    super(Day04, self).__init__(4)

  def parse_data(self):
    return tuple(int(x) for x in self.raw_data[0].split("-"))

  def count_possibilities(self, is_valid):
    possibilities = 0
    for candidate in range(self.data[0], self.data[1]+1):
      if is_valid(candidate):
        possibilities += 1
    return possibilities

  def part_1(self):
    def is_valid(candidate):
      has_double_digit = False
      no_decrease = True

      candidate_str = str(candidate)

      for i, char in enumerate(candidate_str):
        if i == len(candidate_str)-1:
          continue

        if char == candidate_str[i+1]:
          has_double_digit = True
        if char > candidate_str[i+1]:
          no_decrease = False

      return has_double_digit and no_decrease
    return self.count_possibilities(is_valid)

  @property
  def part_1_solution(self):
    return 2150

  def part_2(self):
    def is_valid(candidate):
      has_double_digit = False
      no_decrease = True

      candidate_str = str(candidate)

      for i, char in enumerate(candidate_str):
        if i == len(candidate_str)-1:
          continue

        if char == candidate_str[i+1] and \
            (i == 0 or char != candidate_str[i-1]) and \
            (i == len(candidate_str)-2 or char != candidate_str[i+2]):
          has_double_digit = True
        if char > candidate_str[i+1]:
          no_decrease = False

      return has_double_digit and no_decrease
    return self.count_possibilities(is_valid)

  @property
  def part_2_solution(self):
    return 1462
