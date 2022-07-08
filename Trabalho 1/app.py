REGISTERS = ['$0', '$at',
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
  'ori',
  'slti',
  'sltiu',
]

J_TYPE = [
  'j',
  'jal'
]

R_STRUCTURE = ['op', 'rs', 'rt', 'rd', 'shamt', 'funct']
# R_STRUCTURE = {'op': '',
#                'rs': '',
#                'rt': '',
#                'rd': '',
#                'shamt': '',
#                'funct': ''
#               }

I_STRUCTURE = ['op', 'rs', 'rt', 'immediate']

J_STRUCTURE = ['op', 'address']

OPCODES = {
  'R': '000000',
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

def toHex(binaryString):
  binaryString = binaryString.replace(' ', '')
  binaryNumber = int(binaryString, 2)
  return hex(binaryNumber)

def exclude_comma(string):
  return string.replace(',', '')

def get_type(instruction):
  name = instruction.split()[0]
  if name in R_TYPE:
    return 'R'
  if name in I_TYPE:
    return 'I'
  return 'J'

def get_type_structure(type):
  if type == 'R':
    return R_STRUCTURE
  if type == 'I':
    return I_STRUCTURE
  return J_STRUCTURE

def get_register(register):
  decimal_index = REGISTERS.index(register)
  return bin(decimal_index)[2:]

def get_opcode(instruction):
  type = get_type(instruction)
  name = instruction.split()[0]
  if type == 'R':
    return OPCODES['R']
  return OPCODES[name]
  
def get_rs(instruction):
  type = get_type(instruction)
  if type == 'R':
    rs = instruction.split()[2]
  if type == 'I':
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

def mount_R_type(instruction):
  # R_STRUCTURE['op'] = get_opcode(instruction)
  # R_STRUCTURE['rs'] = get_rs(instruction)
  # R_STRUCTURE['rs'] = get_rs(instruction)
  # R_STRUCTURE['rs'] = get_rs(instruction)
  op = get_opcode(instruction)
  rs = get_rs(instruction)
  rt = get_rt(instruction)
  rd = get_rd(instruction)
  shamt = get_shamt(instruction)
  funct = get_funct(instruction)
  print(op, rs, rt, rd, shamt, funct)

instruction = 'add $s0, $s1, $s2'
type = get_type(instruction)
type_structure = get_type_structure(type)

print(instruction)
mount_R_type(instruction)
