#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import permutations

from day import Day
from intcode import Intcode


class Day07(Day):

  def __init__(self):
    super(Day07, self).__init__(7)

  def parse_data(self):
    return self.parse_intcode_data()

  def part_1(self):
    max_output = 0
    for phases in permutations(range(5)):
      outputs = [0]
      for phase in phases:
        intcode = Intcode(self.data[:], inputs=[phase, outputs[-1]], outputs=outputs)
        intcode.compute()

      if outputs[-1] > max_output:
        max_output = outputs[-1]

    return max_output

  @property
  def part_1_solution(self):
    return 914828

  def part_2(self):
    max_output = 0
    for phases in permutations(range(5, 10)):
      inputs = [[phases[i]] for i in range(5)]
      inputs[0].append(0)
      intcodes = [Intcode(self.data[:], inputs=inputs[i], outputs=inputs[(i+1)%5]) for i in range(5)]

      is_finished = False
      while not is_finished:
        is_finished = any([intcode.partial_compute() for intcode in intcodes])

      if inputs[0][-1] > max_output:
        max_output = inputs[0][-1]

    return max_output

  @property
  def part_2_solution(self):
    return 17956613
