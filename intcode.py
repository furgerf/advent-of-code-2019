#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Intcode:

  OPCODE_PARAMETERS = {
      1: 3,
      2: 3,
      3: 1,
      4: 1,
      5: 2,
      6: 2,
      7: 3,
      8: 3,
      99: 0
      }

  def __init__(self, code):
    self.code = code

  @staticmethod
  def _parse_instruction(instruction):
    instruction_str = str(instruction)

    # retrieve opcode and associated number of parameters
    opcode = int(instruction_str[-2:])
    parameter_count = Intcode.OPCODE_PARAMETERS[opcode]

    # add padding to instruction string for parameter modes
    instruction_str = "0" * (2 + parameter_count - len(instruction_str)) + instruction_str

    # extract the mode of the parameters
    parameter_modes = [int(instruction_str[-3-i]) for i in range(parameter_count)]

    return opcode, parameter_modes

  def retrieve_parameters(self, cursor, parameter_modes):
    parameters = []

    for i, parameter_mode in enumerate(parameter_modes):
      parameter_data = self.code[cursor+1+i]
      if parameter_mode == 0: # position
        parameters.append(self.code[parameter_data])
      elif parameter_mode == 1: # immediate
        parameters.append(parameter_data)
      else:
        raise ValueError("Unknown parameter mode: {}".format(parameter_mode))

    return parameters

  def compute(self, inputs=[], outputs=[]):
    cursor = 0
    while True:
      instruction = self.code[cursor]
      opcode, parameter_modes = Intcode._parse_instruction(instruction)
      parameters = self.retrieve_parameters(cursor, parameter_modes)

      old_cursor = cursor
      if opcode == 1: # add
        assert parameter_modes[2] == 0, "always have positional destination"
        self.code[self.code[cursor+3]] = parameters[0] + parameters[1]
        cursor += 1 + len(parameters)
      elif opcode == 2: # multiply
        assert parameter_modes[2] == 0, "always have positional destination"
        self.code[self.code[cursor+3]] = parameters[0] * parameters[1]
        cursor += 1 + len(parameters)
      elif opcode == 3: # input
        assert parameter_modes[0] == 0, "always have positional destination"
        print("Using input '{}'".format(inputs[0]))
        self.code[self.code[cursor+1]] = inputs.pop(0)
        cursor += 1 + len(parameters)
      elif opcode == 4: # output
        print("Adding output '{}'".format(parameters[0]))
        outputs.append(parameters[0])
        cursor += 1 + len(parameters)
      elif opcode == 5: # jump if true
        if parameters[0]:
          cursor = parameters[1]
        else:
          cursor += 1 + len(parameters)
      elif opcode == 6: # jump if false
        if not parameters[0]:
          cursor = parameters[1]
        else:
          cursor += 1 + len(parameters)
      elif opcode == 7: # less than
        assert parameter_modes[2] == 0, "always have positional destination"
        self.code[self.code[cursor+3]] = int(parameters[0] < parameters[1])
        cursor += 1 + len(parameters)
      elif opcode == 8: # equals
        assert parameter_modes[2] == 0, "always have positional destination"
        self.code[self.code[cursor+3]] = int(parameters[0] == parameters[1])
        cursor += 1 + len(parameters)
      elif opcode == 99: # halt
        break
      else:
        raise ValueError("Unknown opcode: {}".format(opcode))

      assert cursor != old_cursor, "forgot to change cursor?"
