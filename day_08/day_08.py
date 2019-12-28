#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from day import Day
from imageio import imwrite


class Day08(Day):

  def __init__(self):
    super(Day08, self).__init__(8)

  def parse_data(self):
    width = 25
    height = 6
    pixels_per_layer = width * height
    pixels = np.array([int(c) for c in self.raw_data[0]])
    return [pixels[i*pixels_per_layer:(i+1)*pixels_per_layer].reshape(width, height)
        for i in range(len(pixels) // pixels_per_layer)]

  def part_1(self):
    fewest_zeros = np.prod(self.data[0].shape)
    min_layer = None

    for layer in self.data:
      zeros = len(np.where(layer == 0)[0])
      if zeros < fewest_zeros:
        fewest_zeros = zeros
        min_layer = layer

    return len(np.where(min_layer == 1)[0]) * \
        len(np.where(min_layer == 2)[0])

  @property
  def part_1_solution(self):
    return 1935

  def part_2(self):
    image = np.full_like(self.data[0], None, dtype=np.object)
    for layer in self.data:
      for index, value in np.ndenumerate(image):
        if value is not None:
          continue
        if layer[index] != 2: # not transparent
          image[index] = layer[index]

    # image = (image.astype(np.uint8) * 255).reshape(self.data[0].shape[1], self.data[0].shape[0], 1)
    # imwrite("day_08/image.png", image)

    return image.sum()

  @property
  def part_2_solution(self):
    return 51
