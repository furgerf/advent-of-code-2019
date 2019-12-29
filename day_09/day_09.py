#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day
from intcode import Intcode


class Day09(Day):

  def __init__(self):
    super(Day09, self).__init__(9)

  def parse_data(self):
    return self.parse_intcode_data()

  def part_1(self):
    intcode = Intcode(self.data[:], inputs=[1])
    intcode.compute()
    assert len(intcode.outputs) == 1
    return intcode.outputs[0]

  @property
  def part_1_solution(self):
    return 4006117640

  def part_2(self):
    intcode = Intcode(self.data[:], inputs=[2])
    intcode.compute()
    assert len(intcode.outputs) == 1
    return intcode.outputs[0]

  @property
  def part_2_solution(self):
    return 88231
