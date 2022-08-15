from tokenize import Number


REGISTERS = ['$zero', '$at',
             '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
             '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
             '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
             '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

R_TYPE = [
  'add',
  'addu',
  'and',
  'break',
  'div',
  'divu',
  'jalr',
  'jr',
  'mfhi',
  'mflo',
  'movn',
  'mthi',
  'mtlo',
  'mult',
  'multu',
  'nor',
  'or',
  'sll',
  'sllv',
  'slt',
  'sltu',
  'sra',
  'srav',
  'srl',
  'srlv',
  'sub',
  'subu',
  'syscall',
  'xor',
]

I_TYPE = [
  'addi',
  'addiu',
  'andi',
  'beq',
  'bgez',
  'bgtz',
  'blez',
  'bltz',
  'bne',
  'lb',
  'lbu',
  'lh',
  'lhu',
  'lui',
  'lw',
  'lwcl',
  'ori',
  'sb',
  'slti',
  'sltiu',
  'sh',
  'sw',
  'swcl',
  'xori'
]

J_TYPE = [
  'j',
  'jal'
]

STRUCTURES = {
  'R': ['op', 'rs', 'rt', 'rd', 'shamt', 'funct'],
  'I': ['op', 'rs', 'rt', 'immediate'],
  'J': ['op', 'address']
}

OPCODES = {
  'R': '000000',
  'I': {
      'addi': '001000',
      'addiu': '001001',
      'andi': '001100',
      'beq': '000100',
      'bgez': '000001',
      'bgtz': '000111',
      'blez': '000110',
      'bltz': '000001',
      'bne': '000101',
      'lb': '100000',
      'lbu': '100100',
      'lh': '100001',
      'lhu': '100101',
      'lui': '001111',
      'lw': '100011',
      'lwc1': '110001',
      'ori': '001101',
      'sb': '101000',
      'slti': '001010',
      'sltiu': '001011',
      'sh': '101001',
      'sw': '101011',
      'swc1': '111001',
      'xori': '001110'
  },
  'J': {
    'j' : '000010',
    'jal' : '000011'
  }
}

R_FUNCTION_CODES = {
  'add': '100000',
  'addu': '100001',
  'and': '100100',
  'break': '001101',
  'div': '011010',
  'divu': '011011',
  'jalr': '001001',
  'jr': '001000',
  'mfhi': '010000',
  'mflo': '010010',
  'movn': '001011',
  'mthi': '010001',
  'mtlo': '010011',
  'mult': '011000',
  'multu': '011001',
  'nor': '100111',
  'or': '100101',
  'sll': '000000',
  'sllv': '000100',
  'slt': '101010',
  'sltu': '101011',
  'sra': '000011',
  'srav': '000111',
  'srl': '000010',
  'srlv': '000110',
  'sub': '100010',
  'subu': '100011',
  'syscall': '001100',
  'xor': '100110',
}

specials = ['lw', 'sw', 'lb', 'sb']

def toHex(binaryString):
  binaryString = binaryString.replace(' ', '')
  binaryNumber = int(binaryString, 2)
  return hex(binaryNumber)[2:]

def exclude_comma(string):
  return string.replace(',', '')

def get_type(instruction):
  name = instruction.split()[0]
  if name in R_TYPE:
    return 'R'
  if name in I_TYPE:
    return 'I'
  return 'J'

def make_it_n_bits(binary, size):
  if len(binary) < size:
    binary = '0' + binary
    new_binary = make_it_n_bits(binary, size)
  else:
    new_binary = binary
  return new_binary

def get_register(register):
  decimal_index = REGISTERS.index(register)
  binary = bin(decimal_index)[2:]
  return make_it_n_bits(binary, 5)

def get_opcode(instruction):
  type = get_type(instruction)
  name = instruction.split()[0]
  if type == 'R':
    return OPCODES['R']
  return OPCODES[type][name]
  
def get_rs(instruction):
  name = instruction.split()[0]
  type = get_type(instruction)
  if type == 'R':
    rs = instruction.split()[2]
  if type == 'I':
    if name in specials:
      rs = instruction.split()[2][-4:-1]
    else:
      rs = instruction.split()[2]
  rs = exclude_comma(rs)
  return get_register(rs)

def get_rd(instruction):
  type = get_type(instruction)
  if type == 'R':
    rd = instruction.split()[1]
  rd = exclude_comma(rd)
  return get_register(rd)

def get_rt(instruction):
  type = get_type(instruction)
  if type == 'R':
    rt = instruction.split()[3]
  if type == 'I':
      rt = instruction.split()[1]
  rt = exclude_comma(rt)
  return get_register(rt)

def get_shamt(instruction):
  type = get_type(instruction)
  if type == 'R':
    return '00000'

def get_funct(instruction):
  type = get_type(instruction)
  command = instruction.split()[0]
  if type =='R':
    return R_FUNCTION_CODES[command]

def get_immediate(instruction):
  name = instruction.split()[0]
  if name in specials:
    binary = bin(int((instruction.split()[-1])[:-5]))[2:]
  else:
    binary = bin(int(instruction.split()[-1]))[2:]
  return make_it_n_bits(binary, 16)

def get_address(instruction):
  binary = bin(int(instruction.split()[1]))[2:-2]
  return make_it_n_bits(binary, 26)

def mount_instruction(instruction):
  type = get_type(instruction)
  structure = STRUCTURES.get(type)
  binary_set = []
  for field in structure:
    if field == 'op':
      x = get_opcode(instruction)
    if field == 'rs':
      x = get_rs(instruction)
    if field == 'rt':
      x = get_rt(instruction)
    if field == 'rd':
      x = get_rd(instruction)
    if field == 'shamt':
      x = get_shamt(instruction)
    if field == 'funct':
      x = get_funct(instruction)
    if field == 'immediate':
      x = get_immediate(instruction)
    if field == 'address':
      x = get_address(instruction)
    binary_set.append(x)
  return binary_set

def convert_instruction_index(index):
  index = toHex(bin(index))
  index = make_it_n_bits(index, 8)
  return index

def print_instructions(mounted_instruction, index, line):
  legible_instruction = ''
  for each_binary in mounted_instruction:
    legible_instruction = legible_instruction + each_binary
  legible_instruction = toHex(legible_instruction)
  legible_instruction = make_it_n_bits(legible_instruction, 8)
  instruction_number = convert_instruction_index(index)
  output_line = "{} : {}; {}: {}".format(instruction_number, legible_instruction, index, line)

  return output_line

def print_data(line, line_index, reference_index=0):
  name = ''
  data_type = ''
  data = ''
  final_line = ''
  all_data = []
  hex_data = ''
  inner_index = reference_index
  for index, content in enumerate(line.split()):
    if index == 0:
      name = line.split()[0]
      name = name[:-1]
    elif index == 1:
      data_type = line.split()[1]
    else: 
      data = line.split()[index]
      if data[-1] == ',':
        data = data[:-1]
      if data[:2] == '0x':
        data = data[2:]
      else:
        int_data = int(data)
        data = hex(int_data)[2:]
      str_inner_index = str(inner_index)
      final_line = '{} : {};\n'.format(make_it_n_bits(str_inner_index, 8), make_it_n_bits(data, 8))
      inner_index = inner_index + 1
      all_data.append(final_line)
  return all_data, inner_index

def main():
  input_file = open("example_saida.asm", "r")
  file_lines = input_file.readlines()

  list_of_instructions = map(mount_instruction, file_lines)

  file_text = open("example_saida_text.mif", "w")
  file_data = open("example_saida_data.mif", "w")

  file_text.write("""DEPTH = 16384;
WIDTH = 32;
ADDRESS_RADIX = HEX;
DATA_RADIX = HEX;
CONTENT
BEGIN\n\n""")
  file_data.write("""DEPTH = 16384;
WIDTH = 32;
ADDRESS_RADIX = HEX;
DATA_RADIX = HEX;
CONTENT
BEGIN\n\n""")

  output_file = file_data
  index = 0
  data_index = 0

  for line in file_lines:
    if line == '\n':
      continue

    if line.split()[0] == '.data':
      continue

    if line.split()[0] == '.text':
      index = 0
      output_file.write('\nEND;')
      output_file = file_text
      continue

    if output_file == file_data:
      str_index = str(index)
      all_data, data_index = print_data(line, index, data_index)
      for each_data in all_data:
        output_file.write(each_data)
      index += 1
      continue

    try:
      mounted_instruction = mount_instruction(line)
      output_line = print_instructions(mounted_instruction, index, line)
      index += 1
      output_file.write(output_line)
    except:
      index += 1
      output_file.write('Instrução não implementada: {}'.format(line))

  output_file.write('\nEND;')

main()