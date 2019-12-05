#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day

class Day02(Day):

  def __init__(self):
    super(Day02, self).__init__(2)

  def parse_data(self):
    return [int(x) for x in self.raw_data[0].split(",")]

  @staticmethod
  def intcode(data, noun, verb):
    data[1] = noun
    data[2] = verb

    cursor = 0
    while True:
      opcode = data[cursor]

      if opcode == 1:
        data[data[cursor+3]] = data[data[cursor+1]] + data[data[cursor+2]]
      elif opcode == 2:
        data[data[cursor+3]] = data[data[cursor+1]] * data[data[cursor+2]]
      elif opcode == 99:
        break
      else:
        raise ValueError("Error 1202")

      cursor += 4

    return data[0]

  def part_1(self):
    print(Day02.intcode(self.data, 12, 2))

  def part_2(self):
    target = 19690720
    for noun in range(100):
      for verb in range(100):
        if Day02.intcode(self.data[:], noun, verb) == target:
          print(noun, verb, 100*noun+verb)
          return
