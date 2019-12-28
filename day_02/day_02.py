#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day
from intcode import Intcode


class Day02(Day):

  def __init__(self):
    super(Day02, self).__init__(2)

  def parse_data(self):
    return self.parse_intcode_data()

  @staticmethod
  def intcode(data, noun, verb):
    data[1] = noun
    data[2] = verb
    intcode = Intcode(data)
    intcode.compute()
    return intcode._code[0]

  def part_1(self):
    return Day02.intcode(self.data[:], 12, 2)

  @property
  def part_1_solution(self):
    return 4570637

  def part_2(self):
    target = 19690720
    for noun in range(100):
      for verb in range(100):
        if Day02.intcode(self.data[:], noun, verb) == target:
          return 100*noun+verb

  @property
  def part_2_solution(self):
    return 5485
