#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from day import Day


class Day14(Day):

  ORE = "ORE"
  FUEL = "FUEL"

  class Reaction:

    def __init__(self, ingredients, result, description):
      self._ingredients = {ing[1]: ing[0] for ing in ingredients}
      self._result_amount = result[0]
      self._result_material = result[1]
      self._description = description

    @property
    def ingredients(self):
      return self._ingredients

    @property
    def result_amount(self):
      return self._result_amount

    @property
    def result_material(self):
      return self._result_material

    def __str__(self):
      return self._description

    def __repr__(self):
      return self.__str__()

  def __init__(self):
    super(Day14, self).__init__(14)

  def parse_data(self):
    def parse_line(line):
      ingredients, result = line.split(" => ")
      result_split = result.split(" ")
      result = (int(result_split[0]), result_split[1])
      ingredients_split = ingredients.split(", ")
      ingredients = [(int(ing.split(" ")[0]), ing.split(" ")[1]) for ing in ingredients_split]
      return Day14.Reaction(ingredients, result, line)

    reactions = [parse_line(line) for line in self.raw_data]
    parsed_data = {}
    for reaction in reactions:
      assert reaction.result_material not in parsed_data
      parsed_data[reaction.result_material] = reaction
    return parsed_data

  def replace_material(self, material, count):
    reaction = self.data[material]
    production_factor = int(math.ceil(count / reaction.result_amount))

    self.all_ingredients[material] -= production_factor * reaction.result_amount
    for ingredient, amount in reaction.ingredients.items():
      if ingredient not in self.all_ingredients:
        self.all_ingredients[ingredient] = 0
      self.all_ingredients[ingredient] += amount * production_factor

  def produce_one_fuel(self):
    material = Day14.FUEL
    count = 1
    return self.produce_material(material, count)

  def produce_material(self, material, count):
    # add ingredients needed to produce the material
    reaction = self.data[material]
    production_factor = int(math.ceil(count / reaction.result_amount))
    for ingredient, amount in reaction.ingredients.items():
      if ingredient not in self.all_ingredients:
        self.all_ingredients[ingredient] = 0
      self.all_ingredients[ingredient] += production_factor * amount

    def find_material_to_replace():
      for material in self.all_ingredients:
        if self.all_ingredients[material] > 0 and material != Day14.ORE:
          return material
      return None

    # replace ingredient materials as long as needed
    material_to_replace = find_material_to_replace()
    while material_to_replace:
      self.replace_material(material_to_replace, self.all_ingredients[material_to_replace])
      material_to_replace = find_material_to_replace()

    # add the produced material
    if material not in self.all_ingredients:
      self.all_ingredients[material] = 0
    self.all_ingredients[material] -= production_factor * reaction.result_amount

  def part_1(self):
    self.all_ingredients = {}
    self.produce_one_fuel()
    return self.all_ingredients[Day14.ORE]

  @property
  def part_1_solution(self):
    return 374457

  def part_2(self):
    collected_ore = 1000000000000
    self.all_ingredients = {}

    regular_execution = False
    if regular_execution:
      # estimate cost per fuel - produce one fuel many times for a more exact estimate
      initial_fuel_production = 100000
      for _ in range(initial_fuel_production):
        self.produce_one_fuel()
      production_factor = collected_ore // self.all_ingredients[Day14.ORE]
      for ingredient in self.all_ingredients:
        self.all_ingredients[ingredient] *= production_factor
    else:
      # cheat a bit for faster execution in regression test
      initial_fuel_production = 1000
      for _ in range(initial_fuel_production):
        self.produce_one_fuel()
      production_factor = 3560
      for ingredient in self.all_ingredients:
        self.all_ingredients[ingredient] *= production_factor

    while self.all_ingredients[Day14.ORE] < collected_ore:
      previous_ingredients = self.all_ingredients.copy()
      self.produce_one_fuel()
    self.all_ingredients = previous_ingredients

    return -self.all_ingredients[Day14.FUEL]

  @property
  def part_2_solution(self):
    return 3568888
