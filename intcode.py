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

  def __init__(self, code, inputs=[], outputs=[], verbose=False):
    self._code = code
    self._inputs = inputs
    self._outputs = outputs
    self._verbose = verbose
    self._cursor = 0

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

  def retrieve_parameters(self, parameter_modes):
    parameters = []

    for i, parameter_mode in enumerate(parameter_modes):
      parameter_data = self._code[self._cursor+1+i]
      if parameter_mode == 0: # position
        parameters.append(self._code[parameter_data])
      elif parameter_mode == 1: # immediate
        parameters.append(parameter_data)
      else:
        raise ValueError("Unknown parameter mode: {}".format(parameter_mode))

    return parameters

  def _process_instruction(self):
    instruction = self._code[self._cursor]
    opcode, parameter_modes = Intcode._parse_instruction(instruction)
    parameters = self.retrieve_parameters(parameter_modes)

    old_cursor = self._cursor
    if opcode == 1: # add
      assert parameter_modes[2] == 0, "always have positional destination"
      self._code[self._code[self._cursor+3]] = parameters[0] + parameters[1]
      self._cursor += 1 + len(parameters)
    elif opcode == 2: # multiply
      assert parameter_modes[2] == 0, "always have positional destination"
      self._code[self._code[self._cursor+3]] = parameters[0] * parameters[1]
      self._cursor += 1 + len(parameters)
    elif opcode == 3: # input
      assert parameter_modes[0] == 0, "always have positional destination"
      if not self._inputs:
        raise IOError("No input to process")
      if self._verbose:
        print("Using input '{}'".format(self._inputs[0]))
      self._code[self._code[self._cursor+1]] = self._inputs.pop(0)
      self._cursor += 1 + len(parameters)
    elif opcode == 4: # output
      if self._verbose:
        print("Adding output '{}'".format(parameters[0]))
      self._outputs.append(parameters[0])
      self._cursor += 1 + len(parameters)
    elif opcode == 5: # jump if true
      if parameters[0]:
        self._cursor = parameters[1]
      else:
        self._cursor += 1 + len(parameters)
    elif opcode == 6: # jump if false
      if not parameters[0]:
        self._cursor = parameters[1]
      else:
        self._cursor += 1 + len(parameters)
    elif opcode == 7: # less than
      assert parameter_modes[2] == 0, "always have positional destination"
      self._code[self._code[self._cursor+3]] = int(parameters[0] < parameters[1])
      self._cursor += 1 + len(parameters)
    elif opcode == 8: # equals
      assert parameter_modes[2] == 0, "always have positional destination"
      self._code[self._code[self._cursor+3]] = int(parameters[0] == parameters[1])
      self._cursor += 1 + len(parameters)
    elif opcode == 99: # halt
      self._cursor = None
    else:
      raise ValueError("Unknown opcode: {}".format(opcode))

    assert self._cursor != old_cursor, "forgot to change cursor?"

  def compute(self):
    assert not self._cursor
    while True:
      self._process_instruction()
      if self._cursor is None:
        break

  def partial_compute(self):
    while True:
      try:
        self._process_instruction()
        if self._cursor is None:
          return True
      except IOError:
        return False
