with open("i-opcodes.txt", 'r') as file:
    input = [] 
    for line in file:
        separate = line.split()
        input.append(" '{}' : '{}' ".format(separate[0], separate[-1]))

    for row in input:
        print('{}'.format(row))
