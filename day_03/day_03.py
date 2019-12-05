#!/usr/bin/env python
# -*- coding: utf-8 -*-

from day import Day

class Day03(Day):

  def __init__(self):
    super(Day03, self).__init__(3)

  def parse_data(self):
    return [
        [(s[0], int(s[1:])) for s in d.split(",")]
        for d in self.raw_data]

  def part_1(self):
    visited = set()
    position = (0, 0)
    for direction, length in self.data[0]:
      if direction == "R":
        for i in range(length):
          visited.add((position[0]+i+1, position[1]))
        position = (position[0]+length, position[1])
      elif direction == "L":
        for i in range(length):
          visited.add((position[0]-i-1, position[1]))
        position = (position[0]-length, position[1])
      elif direction == "U":
        for i in range(length):
          visited.add((position[0], position[1]+i+1))
        position = (position[0], position[1]+length)
      elif direction == "D":
        for i in range(length):
          visited.add((position[0], position[1]-i-1))
        position = (position[0], position[1]-length)
      else:
        raise ValueError()

    position = (0, 0)
    intersections = set()
    for direction, length in self.data[1]:
      if direction == "R":
        for i in range(length):
          if (position[0]+i+1, position[1]) in visited:
            intersections.add((position[0]+i+1, position[1]))
        position = (position[0]+length, position[1])
      elif direction == "L":
        for i in range(length):
          if (position[0]-i-1, position[1]) in visited:
            intersections.add((position[0]-i-1, position[1]))
        position = (position[0]-length, position[1])
      elif direction == "U":
        for i in range(length):
          if (position[0], position[1]+i+1) in visited:
            intersections.add((position[0], position[1]+i+1))
        position = (position[0], position[1]+length)
      elif direction == "D":
        for i in range(length):
          if (position[0], position[1]-i-1) in visited:
            intersections.add((position[0], position[1]-i-1))
        position = (position[0], position[1]-length)
      else:
        raise ValueError()

    distances = [x+y for x, y in intersections]

    print(len(intersections), min(distances))

  def part_2(self):
    visited = {}
    position = (0, 0)
    travelled = 0
    for direction, length in self.data[0]:
      if direction == "R":
        for i in range(length):
          key = (position[0]+i+1, position[1])
          if key not in visited:
            visited[key] = travelled+i+1
        position = (position[0]+length, position[1])
      elif direction == "L":
        for i in range(length):
          key = (position[0]-i-1, position[1])
          if key not in visited:
            visited[key] = travelled+i+1
        position = (position[0]-length, position[1])
      elif direction == "U":
        for i in range(length):
          key = (position[0], position[1]+i+1)
          if key not in visited:
            visited[key] = travelled+i+1
        position = (position[0], position[1]+length)
      elif direction == "D":
        for i in range(length):
          key = (position[0], position[1]-i-1)
          if key not in visited:
            visited[key] = travelled+i+1
        position = (position[0], position[1]-length)
      else:
        raise ValueError()
      travelled += length

    position = (0, 0)
    travelled = 0
    distances = []
    for direction, length in self.data[1]:
      if direction == "R":
        for i in range(length):
          key = (position[0]+i+1, position[1])
          if key in visited:
            distances.append(visited[key]+travelled+i+1)
            del visited[key]
        position = (position[0]+length, position[1])
      elif direction == "L":
        for i in range(length):
          key = (position[0]-i-1, position[1])
          if key in visited:
            distances.append(visited[key]+travelled+i+1)
            del visited[key]
        position = (position[0]-length, position[1])
      elif direction == "U":
        for i in range(length):
          key = (position[0], position[1]+i+1)
          if key in visited:
            distances.append(visited[key]+travelled+i+1)
            del visited[key]
        position = (position[0], position[1]+length)
      elif direction == "D":
        for i in range(length):
          key = (position[0], position[1]-i-1)
          if key in visited:
            distances.append(visited[key]+travelled+i+1)
            del visited[key]
        position = (position[0], position[1]-length)
      else:
        raise ValueError()
      travelled += length

    print(len(distances), min(distances))
