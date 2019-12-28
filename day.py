#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod


class Day(ABC):
  def __init__(self, day_number):
    self.day_number = day_number
    self.raw_data = self.load_data()
    self.data = self.parse_data()

  def load_data(self):
    file_name = os.path.join("day_{:02d}".format(self.day_number), "input")
    with open(file_name) as fh:
      return [line.rstrip() for line in fh.readlines()]

  @abstractmethod
  def parse_data(self):
    pass

  def parse_intcode_data(self):
    assert len(self.raw_data) == 1
    return [int(x) for x in self.raw_data[0].split(",")]

  @abstractmethod
  def part_1(self):
    pass

  @property
  @abstractmethod
  def part_1_solution(self):
    pass

  @abstractmethod
  def part_2(self):
    pass

  @property
  @abstractmethod
  def part_2_solution(self):
    pass
