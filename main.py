from classes import *
import csv

outBlock = BlocoDeSaida()


mneList = list()
with open('mnemonicos.txt') as pseudoInstructionsFile:
    pseudoInstructions = csv.reader(pseudoInstructionsFile, delimiter=',')

    for line in pseudoInstructions:
        if line[0] == '@':
            mneList.append(Mnemonic(line[0], line[1], None, line[3], line[4]))
        else: 
            mneList.append(Mnemonic(line[0], line[1], int(line[2]), line[3], line[4]))

symbolTable = Table[Symbol]([])
mneTable = Table[Mnemonic](genericList=mneList)

print()
print("Tabela de Mneumônicos")
print()
print("{:<8} {:<5} {:<4} {:<10} {:<10}".format('mnemonic', 'code', 'size', 'mneType', 'operand'))
print(mneTable)

with open('teste.txt') as programaFonte:
    
    program = programaFonte.readlines()
    CI = 0
    for l in program:

        ## PASSO 1
        line = Line(l)

        # Tratamento do Rótulo
        if line.rotulo != '':

            # tenta puxar da tabela
            s = symbolTable.get(line.rotulo)

            # não existe na tabela
            if s == None:
                s = Symbol(line.rotulo, 'ADDRESS')
                symbolTable.add(s)

            # existe e já estava definido -> (ERRO)
            elif s.defined: 
                raise Exception('Symbol already defined')
            
            s.address = hex(CI)
            s.define()              # seta definido
            symbolTable.set(s)      # atualiza tabela

        

        ## PASSO 2
        
        # propcura mneumônico
        mne = mneTable.get(line.mne)
        if mne == None:
            raise Exception("Mneumonic " + mne + " not defined")
        
        # atualiza CI
        CI += mne.size()
        if mne._operand == "address":
            isSymbol = False
            try:
                address = hex(line.op)
            except:
                isSymbol = True
                address = line.op

            if isSymbol:
                s = Symbol(name = line.op, symbolType='ADDRESS')

        op = line.op

        
        
        size = mne.size()

        outBlock.add(hex(CI), mne._code, line.rotulo, mne._mnemonic, op)
        


print()
print("Tabela de simbolos")
print(symbolTable)

print()
print(outBlock)