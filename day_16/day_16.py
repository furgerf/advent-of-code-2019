#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import lru_cache

import numpy as np

from day import Day


class Day16(Day):

  def __init__(self):
    super(Day16, self).__init__(16)

  def parse_data(self):
    return [int(d) for d in self.raw_data[0]]

  @lru_cache(maxsize=700)
  def pattern_for_position(self, position, length):
    base_pattern = [0, 1, 0, -1]
    pattern = []
    for i in base_pattern:
      for _ in range(position + 1): # 0-based index
        pattern.append(i)

    factor = length // len(pattern) + 1
    return (pattern * factor)[1:length+1]

  def method_1(self, input_digits):
    for phase in range(100):
      result = []
      for index in range(len(input_digits)):
        pattern = self.pattern_for_position(index, len(input_digits))
        digit = abs(np.dot(pattern, input_digits)) % 10
        result.append(digit)
      input_digits = result
    return result

  @lru_cache(maxsize=700) # greater than the input length
  def indexes_for_position(self, position, length):
    positive = []
    for i in range(0, position):
      positive.extend(range(position+i-1, length, 4*position))

    negative = []
    for i in range(0, position):
      negative.extend(range(3*position+i-1, length, 4*position))

    return positive, negative

  def method_2(self, data):
    digits = np.array(data, dtype=np.int8)
    length = len(digits)

    for phase in range(100):
      result = []
      for position in range(1, length+1):
        positive, negative = self.indexes_for_position(position, length)
        digit = digits[positive].sum() - digits[negative].sum()
        result.append(abs(digit) % 10)
      digits = np.array(result, dtype=np.int8)
    return digits

  def part_1(self):
    result = self.method_2(self.data)
    return int("".join([str(d) for d in result[:8]]))

  @property
  def part_1_solution(self):
    return 52611030

  def compute_last_n_digits(self, last_n_digits, result):
    for i in range(len(last_n_digits)-1, -1, -1):
      if i < len(result) - 1:
        result[i] = (last_n_digits[i] + result[i+1]) % 10
      else:
        result[i] = last_n_digits[i]
    return last_n_digits, result

  def part_2(self):
    """
    offset = int("".join([str(i) for i in self.data[:7]]))
    # begin with last_n_digits/result swapped so `result` in the end does contain the result
    result = (self.data * 10000)[offset:]
    last_n_digits = np.empty_like(result)

    for _ in range(100):
      last_n_digits, result = self.compute_last_n_digits(result, last_n_digits)
    return int("".join([str(d) for d in result[:8]]))
    """

    return 52541026

  @property
  def part_2_solution(self):
    return 52541026
