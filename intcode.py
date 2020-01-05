#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Intcode:

  class Parameter:

    def __init__(self, index, value):
      self._index = index
      self._value = value

    @property
    def index(self):
      if self._index is None:
        raise RuntimeError()
      return self._index

    @property
    def value(self):
      return self._value

    def __str__(self):
      return "code[{}]={}".format(self._index, self._value)

    def __repr__(self):
      return self.__str__()

  OPCODE_PARAMETERS = {
      1: 3,
      2: 3,
      3: 1,
      4: 1,
      5: 2,
      6: 2,
      7: 3,
      8: 3,
      9: 1,
      99: 0
      }

  def __init__(self, code, inputs=None, outputs=None, verbose=False):
    self._code = code
    self._inputs = inputs or []
    self._outputs = outputs or []
    self._verbose = verbose
    self._cursor = 0
    self._relative_base = 0

  @property
  def outputs(self):
    return self._outputs

  def clear_output(self):
    self._outputs = []

  def add_input(self, new_input):
    if isinstance(new_input, list):
      self._inputs.extend(new_input)
    else:
      self._inputs.append(new_input)

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

  def _ensure_sufficient_memory(self, required_index):
    additional_memory = [0] * (required_index - len(self._code) + 1)
    self._code.extend(additional_memory)
    if self._verbose and additional_memory:
      print("Adding {} cells of memory to {}".format(
        len(additional_memory), len(self._code)))

  def retrieve_parameters(self, parameter_modes):
    parameters = []

    for i, parameter_mode in enumerate(parameter_modes):
      parameter_data = self._code[self._cursor+1+i]
      if parameter_mode == 0: # position
        self._ensure_sufficient_memory(parameter_data)
        parameters.append(Intcode.Parameter(parameter_data, self._code[parameter_data]))
      elif parameter_mode == 1: # immediate
        parameters.append(Intcode.Parameter(None, parameter_data))
      elif parameter_mode == 2: # relative
        position = self._relative_base + parameter_data
        self._ensure_sufficient_memory(position)
        parameters.append(Intcode.Parameter(position, self._code[position]))
      else:
        raise ValueError("Unknown parameter mode: {}".format(parameter_mode))

    return parameters

  def _process_instruction(self):
    instruction = self._code[self._cursor]
    opcode, parameter_modes = Intcode._parse_instruction(instruction)
    parameters = self.retrieve_parameters(parameter_modes)

    old_cursor = self._cursor
    if self._verbose:
      print("  OP {}, modes {}, params {}".format(opcode, parameter_modes, parameters))

    if opcode == 1: # add
      if self._verbose:
        print("    Writing {}+{} to {}".format(
          parameters[0].value, parameters[1].value, parameters[2].index))
      self._code[parameters[2].index] = parameters[0].value + parameters[1].value
      self._cursor += 1 + len(parameters)
    elif opcode == 2: # multiply
      self._ensure_sufficient_memory(self._code[self._cursor+3])
      if self._verbose:
        print("    Writing {}*{} to {}".format(
          parameters[0].value, parameters[1].value, parameters[2].index))
      self._code[parameters[2].index] = parameters[0].value * parameters[1].value
      self._cursor += 1 + len(parameters)

    elif opcode == 3: # input
      if not self._inputs:
        raise IOError("No input to process")
      if self._verbose:
        print("    Writing input {} to {}".format(self._inputs[0], parameters[0].index))
      self._ensure_sufficient_memory(parameters[0].index)
      self._code[parameters[0].index] = self._inputs.pop(0)
      self._cursor += 1 + len(parameters)
    elif opcode == 4: # output
      if self._verbose:
        print("    Adding output {}".format(parameters[0].value))
      self._outputs.append(parameters[0].value)
      self._cursor += 1 + len(parameters)

    elif opcode == 5: # jump if true
      if self._verbose:
        print("    Jumping if {} to {}".format(parameters[0].value, parameters[1].value))
      if parameters[0].value:
        self._cursor = parameters[1].value
      else:
        self._cursor += 1 + len(parameters)
    elif opcode == 6: # jump if false
      if self._verbose:
        print("    Jumping if NOT {} to {}".format(parameters[0].value, parameters[1].value))
      if not parameters[0].value:
        self._cursor = parameters[1].value
      else:
        self._cursor += 1 + len(parameters)

    elif opcode == 7: # less than
      if self._verbose:
        print("    Writing {}<{} to {}".format(
          parameters[0].value, parameters[1].value, parameters[2].index))
      self._code[parameters[2].index] = int(parameters[0].value < parameters[1].value)
      self._cursor += 1 + len(parameters)
    elif opcode == 8: # equals
      if self._verbose:
        print("    Writing {}=={} to {}".format(
          parameters[0].value, parameters[1].value, parameters[2].index))
      self._code[parameters[2].index] = int(parameters[0].value == parameters[1].value)
      self._cursor += 1 + len(parameters)

    elif opcode == 9: # adjust relative base
      if self._verbose:
        print("    Adding {} to relative base".format(parameters[0].value))
      self._relative_base += parameters[0].value
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
    """
    Runs until a new input is required.

    Returns:
      True if the program halted and False if a new input is required.
    """
    while True:
      try:
        self._process_instruction()
        if self._cursor is None:
          return True
      except IOError:
        return False
