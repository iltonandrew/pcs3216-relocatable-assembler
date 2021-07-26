from classes import *
import csv

mneList = list([Mnemonic('LD', '0000', 'memoryRead'), Mnemonic('ADD', '0001', 'arithimetic')])

symbolTable = Table[Symbol]([])
mneTable = Table[Mnemonic](genericList=mneList)

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

        ## PASSO 2

print(symbolTable)
print(mneTable)