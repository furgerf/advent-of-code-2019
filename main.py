#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser
from importlib import import_module
from time import time

import numpy as np

from day import Day


def parse_arguments():
  parser = ArgumentParser()

  parser.add_argument("-d", "--day", required=True, type=int)
  parser.add_argument("-1", "--part-1", action="store_true")
  parser.add_argument("-2", "--part-2", action="store_true")

  return parser.parse_args()

def main():
  args = parse_arguments()

  directories = [name for name in os.listdir(".")
      if os.path.isdir(name) and name == "day_{:02d}".format(args.day)]
  assert len(directories) == 1
  import_module("{name}.{name}".format(name=directories[0]))
  assert len(Day.__subclasses__()) == 1

  day = Day.__subclasses__()[0]()

  if args.part_1:
    day.part_1()

  if args.part_2:
    day.part_2()

if __name__ == "__main__":
  START_TIME = time()
  main()
  print("Evaluation time {:.1f}s".format((time() - START_TIME)))
