from classes import *
import csv

mneList = list()
with open('pseudo.txt') as pseudoInstructionsFile:
    pseudoInstructions = csv.reader(pseudoInstructionsFile, delimiter=',')

    for line in pseudoInstructions:

        mneList.append(Mnemonic(line[0], line[1], line[2], line[3], line[4], line[5]))

symbolTable = Table[Symbol]([])
mneTable = Table[Mnemonic](genericList=mneList)

print()
print("Tabela de Mneumônicos")
print(mneTable)

# print(item._mnemonic)

with open('teste.txt') as programaFonte:
    
    program = csv.reader(programaFonte, delimiter=',')
    for line in program:

        ## PASSO 1

        # Tratamento do Rótulo
        if line[0] != '':

            # tenta puxar da tabela
            s = symbolTable.get(line[0])

            # não existe na tabela
            if s == None:
                s = Symbol(line[0], 'type1')
                symbolTable.add(s)

            # existe e já estava definido (ERRO)
            elif s.defined: 
                raise Exception('Symbol already defined')
            
            s.address = '0001'      # add endereço CI
            s.define()              # seta definido
            symbolTable.set(s)      # atualiza tabela

        # Analisar mneumônico
        name = line[1]
        v = line[2]
        op = line[3]

        mne = mneTable.get(name)
        if mne == None:
            raise Exception("Mneumonic " + name + " not defined")
        print("size: " + str(mne.size()) + " bytes")

        ## PASSO 2
print()
print("Tabela de simbolos")
print(symbolTable)