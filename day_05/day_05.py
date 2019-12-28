#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day
from intcode import Intcode


class Day05(Day):

  def __init__(self):
    super(Day05, self).__init__(5)

  def parse_data(self):
    return self.parse_intcode_data()

  def part_1(self):
    intcode = Intcode(self.data[:], inputs=[1])
    intcode.compute()
    assert sum(intcode.outputs[:-1]) == 0
    return intcode.outputs[-1]

  @property
  def part_1_solution(self):
    return 9938601

  def part_2(self):
    intcode = Intcode(self.data[:], inputs=[5])
    intcode.compute()
    return intcode.outputs[-1]

  @property
  def part_2_solution(self):
    return 4283952
