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
    intcode = Intcode(self.data[:])
    intcode.compute([1], [])

  def part_2(self):
    intcode = Intcode(self.data[:])
    intcode.compute([5], [])
