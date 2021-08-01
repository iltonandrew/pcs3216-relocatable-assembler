from classes import *
import csv

outBlock = BlocoDeSaida()


mneList = list()
with open('mnemonicos.txt') as pseudoInstructionsFile:
    pseudoInstructions = csv.reader(pseudoInstructionsFile, delimiter=',')

    for line in pseudoInstructions:
        if 'tag' in line[5]:
            mneList.append(Mnemonic(line[0], line[1], None, line[3], line[4]))
        elif 'instruction' in line[5]:
            mneList.append(OperandMnemonic(line[0], line[1], int(line[2]), line[3], line[4]))
        else: 
            mneList.append(Mnemonic(line[0], line[1], int(line[2]), line[3], line[4]))

symbolTable = Table[Symbol]([])
mneTable = Table[Mnemonic](genericList=mneList)

print()
print("Tabela de Mneumônicos")
print()
print("{:<8} {:<5} {:<4} {:<10} {:<10}".format('mnemonic', 'code', 'size', 'mneType', 'operand'))
print(mneTable)

passo = 1
# PASSO 1
with open('teste.txt') as programaFonte:
    
    program = programaFonte.readlines()
    CI = 0

    print(program)


# PASSO 2
with open('teste.txt') as programaFonte:
    
    program = programaFonte.readlines()
    CI = 0

    print(program)


