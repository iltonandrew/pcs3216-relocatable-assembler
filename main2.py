from classes import *
import csv

arqTeste = "somaVetor4.txt"
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
with open(arqTeste) as programaFonte:
    
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
            equ = Symbol(linha[1], 'equivalencia')
            equ.value = linha[2]
            equ.define()
            if not symbolTable.get(linha[1]):
                symbolTable.add(equ)
            else:
                symbolTable.set(equ)
            

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

# Check Symbol Table

# Write obj-program header on saida.txt file

saida = open("saida.txt", "w")
saida.write("Tabela de simbolos\n")
saida.write("{:<8} {:<8} {:<5} {:<4} {:<10}\n".format('Nome', 'Endereço', 'Valor', 'I/D', 'Tipo'))
saida.write(str(symbolTable))


# PASSO 2
print('passo 2')
with open(arqTeste) as programaFonte:

    CI = 0
    
    for l in program:
        linha = l.split()

        instruc = mneTable.get(linha[0])
        rotulo = ""

        # tem rótulo?
        if instruc == None:
            # linha[0] é rótulo
            rotulo = symbolTable.get(linha[0])

            linha.pop(0)
            instruc = mneTable.get(linha[0])

        # é pseudo?
        if instruc._type == 'ORG':
            CI = int(linha[1], 16)
        
        elif instruc._type == 'END':
            pass            
        
        elif instruc._type == 'EQU':            
            pass
            

        elif instruc._type == 'DBDWDA':
            #define uma constante na memoria
            operando = linha[1]

            s = symbolTable.get(operando)
            if s:
                operando = s.address
                size = 1
            else:
                size = int(operando) // 256 + 1
                operando = operando.zfill(size*2)

            rotulo = rotulo._name if rotulo !=  "" else ""
            outBlock.add(hex(CI), operando, rotulo, linha[0], linha[1])
            CI += size

        elif instruc._type == 'BLOC':

            rotulo = rotulo._name if rotulo !=  "" else ""
            outBlock.add(hex(CI), "00", rotulo, linha[0], linha[1])
            CI += 1
            for i in range(int(linha[1])-1):
                outBlock.add(hex(CI), "00", "", "", "")
                CI += 1

        elif instruc._type == 'NAME':
            pass

        elif instruc._type == 'ENTRY':
            pass

        elif instruc._type == 'EXTERNAL':
            pass
                
        # não é pseudo
        else: 
            s = symbolTable.get(linha[1]) #procura operando na tab simbolos, assumindo q sempre vai ser simbolo
            codigo = instruc._code + s.address[2:]
            rotulo = rotulo._name if rotulo !=  "" else ""
            outBlock.add(hex(CI), codigo, rotulo, linha[0], linha[1])
            CI += instruc._size
            
print()
print("Bloco de saida")
print()
print("{:<8} {:<5} {:<4} {:<10} {:<10}".format('CI', 'codigo', 'rotulo', 'mnemonico', 'operand'))
print(outBlock)


# Write obj-program on saida.txt file

saida.write("Bloco de saida\n")
saida.write("{:<8} {:<5} {:<4} {:<10} {:<10}\n".format('CI', 'codigo', 'rotulo', 'mnemonico', 'operand'))
saida.write(str(outBlock))
saida.close()

