#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day

class Day01(Day):

  def __init__(self):
    super(Day01, self).__init__(1)

  def parse_data(self):
    return [int(line) for line in self.raw_data]

  @staticmethod
  def calculate_fuel(weight):
    return max(weight // 3 - 2, 0)

  def part_1(self):
    fuel_costs = [Day01.calculate_fuel(weight) for weight in self.data]
    return sum(fuel_costs)

  @property
  def part_1_solution(self):
    return 3423511

  def part_2(self):
    def recursive_calculate_fuel(weight, current_fuel_cost):
      new_fuel = Day01.calculate_fuel(weight)
      if new_fuel == 0:
        return current_fuel_cost
      return recursive_calculate_fuel(new_fuel, current_fuel_cost + new_fuel)

    fuel_costs = [recursive_calculate_fuel(weight, 0) for weight in self.data]
    return sum(fuel_costs)

  @property
  def part_2_solution(self):
    return 5132379
