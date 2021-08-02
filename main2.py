from classes import *
import csv

outBlock = BlocoDeSaida()

mneList = list()
with open('mnemonicos.txt') as pseudoInstructionsFile:
    pseudoInstructions = csv.reader(pseudoInstructionsFile, delimiter=',')

    for line in pseudoInstructions:
        if 'pseudo' in line[5]:
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
print('passo 1')
with open('teste.txt') as programaFonte:
    
    program = programaFonte.readlines()
    CI = 0

    for l in program:

        linha = l.split()

        instruc = mneTable.get(linha[0])

        # tem rótulo?
        if instruc == None:
            # linha[0] é rótulo
            rotulo = linha[0]
            s = Symbol(rotulo, "interno")
            sOnTable = symbolTable.get(rotulo)
            
            if sOnTable:
                s = sOnTable
            else:
                symbolTable.add(s)
    
            if s.defined:
                raise Exception('Symbol already defined')
            
            s.address = hex(CI)
            s.define()              # seta definido
            symbolTable.set(s)      # atualiza tabela

            linha.pop(0)
            instruc = mneTable.get(linha[0])

        
        # é pseudo?
        if instruc._type == 'ORG':
            CI = int(linha[1], 16)
        
        elif instruc._type == 'END':
            if not symbolTable.get('Módulo'):
                s = Symbol('Módulo', 'nome')
                s.value = "Início"
                s.define()
                symbolTable.add(s)
            else:
                s = symbolTable.get('Módulo')
            
            address = 0 if len(linha) == 1 else (symbolTable.get(linha[1]).address if symbolTable.get(linha[1]) else int(linha[1], 16))
            s.address = address

            symbolTable.set(s)

            passo = 2
            print("O programa se inicia no simbolo ",linha[1])
            break
        
        elif instruc._type == 'EQU':
            address = symbolTable.get(linha[2]).address if symbolTable.get(linha[2]) else int(linha[2], 16)
            equ = Symbol(linha[1], 'equivalencia')
            equ.value = linha[2]
            equ.define()
            symbolTable.add(equ)
            

        elif instruc._type == 'DBDWDA':
            CI += 1

        elif instruc._type == 'BLOC':
            CI += int(linha[1])
            print("Reserva de " + linha[1] + " bytes na memória")

        elif instruc._type == 'NAME':
            if not symbolTable.get(linha[1]):
                s = Symbol('Módulo', 'nome')
                s.address = hex(CI)
                s.value = linha[1]
                s.define()
                symbolTable.add(s)
            else:
                raise Exception('Simbolo {s} já foi definido'.format(linha[1]))

        elif instruc._type == 'ENTRY':
            # falta gerar o bloco de entry points no saida.txt
            for entryPoint in linha[1:]:
                if not symbolTable.get(entryPoint):
                    s = Symbol(entryPoint, 'público')
                    symbolTable.add(s)
                else:
                    s = symbolTable.get(entryPoint)
                    s._type = 'público'

        elif instruc._type == 'EXTERNAL':
            # falta gerar o bloco de externals no saida.txt
            for entryPoint in linha[1:]:
                if not symbolTable.get(entryPoint):
                    s = Symbol(entryPoint, 'externo')
                    symbolTable.add(s)
                else:
                    s = symbolTable.get(entryPoint)
                    s._type = 'externo'
                s.define()
                
        # não é pseudo
        else:
            CI += instruc.size()
        
        print("CI atualizado para ", hex(CI))


print()
print("Tabela de simbolos")
print("{:<8} {:<8} {:<5} {:<4} {:<10}".format('Nome', 'Endereço', 'Valor', 'I/D', 'Tipo'))
print(symbolTable)

# PASSO 2
print('passo 2')
with open('teste.txt') as programaFonte:
    
    for l in program:
        linha = l.split()

        instruc = mneTable.get(linha[0])

        # tem rótulo?
        if instruc == None:
            # linha[0] é rótulo
            rotulo = symbolTable.get(linha[0])

            '''
                Your code here
            '''

            linha.pop(0)
            instruc = mneTable.get(linha[0])

        # é pseudo?
        if instruc._type == 'ORG':

            '''
                Your code here
            '''
            
            pass
        
        elif instruc._type == 'END':

            '''
                Your code here
            '''
            
            pass
        
        elif instruc._type == 'EQU':

            '''
                Your code here
            '''
            
            pass
            

        elif instruc._type == 'DBDWDA':

            '''
                Your code here
            '''
            
            pass

        elif instruc._type == 'BLOC':

            '''
                Your code here
            '''
            
            pass

        elif instruc._type == 'NAME':

            '''
                Your code here
            '''
            
            pass

        elif instruc._type == 'ENTRY':

            '''
                Your code here
            '''
            
            pass

        elif instruc._type == 'EXTERNAL':

            '''
                Your code here
            '''
            
            pass
                
        # não é pseudo
        else:

            '''
                Your code here
            '''
            
            pass


