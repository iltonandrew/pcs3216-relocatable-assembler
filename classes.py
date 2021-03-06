from typing import Generic, List,TypeVar
T = TypeVar("T")

class Symbol:
    def __init__(self, name: str,  symbolType: str):
        self._name = name
        self.address = None
        self._type = symbolType
        self.defined = False
        self.references = []
        self.value = None

    def define(self):
        self.defined = True
    
    def __str__(self):
        return "{:<8} {:<8} {:<11} {:<4} {:<10}".format(self._name, (self.address if self.address else '-'), (self.value if self.value else '-'), ('D' if self.defined else 'I'), self._type)
    
    def __eq__(self, other):
    
       if other == self._name:
           return True
       return False
    
    def key(self):
        return self._name;
    
    def __hash__(self):
        return hash(self._name)

class Mnemonic:

    def __init__(self,
                mnemonic: str,
                code: int,
                size: int,
                name: str,
                operand: str,
                mneType: str):
        self._mnemonic = mnemonic.strip()
        self._code = code if code else '-'
        self._size = size if size != None else 0
        self._name = name.strip()
        self._type = mneType.strip()
        self._operand = operand.strip()

    def __str__(self):
        return "{:<8} {:<5} {:<4} {:<10} {:<11} {:<10}".format(self._mnemonic,self._code,self._size,self._name,self._operand,self._type)

    def size(self):
        return self._size
    
    def code(self, address:str):
        return self._code

    def __eq__(self, other):
       if other == self._mnemonic:
           return True
       return False
    
    def key(self):
        return self._mnemonic;
    
    def __hash__(self):
        return hash(self._mnemonic)

class OperandMnemonic(Mnemonic):
    def __init__(self, mnemonic: str, code: int, size: int, name: str, operand: str, mneType: str):
        super().__init__(mnemonic, code, size, name, operand, mneType)
    
    def code(self, address: str):
        return self._code + address

class Table(Generic[T]):

    def __init__(self,  genericList: List[T]):
        self._dict = {}
        for item in genericList:
            self._dict[item.key()] = item
        
    def get(self, key: str) -> T:
        try:
            return self._dict[key]
        except KeyError:
            return None
    
    def set(self, item: T):
        key = item.key()
        if self.get(key) == None: raise Exception("Table does not contains key " + key)
        self._dict[key] = item

    
    def add(self, newItem: T):
        if (self.get(newItem) != None):
            raise Exception("Table already contains item for" + newItem.key())
        self._dict[newItem.key()] = newItem
    
    def __str__(self):
        string = ''
        for line in self._dict.values():
            string += str(line) + '\n'
        return string

class BlocoDeSaida:
    def __init__(self) -> None:
        self._tabela = [['Endere??o', 'c??digo', 'r??tulo', 'Mnem??nico', 'Operando']]

    def add(self, address, cod, rotulo, mne, op):
        line = [address, cod, rotulo, mne, op]
        self._tabela.append(line)

    def insert(self, index, Line):
        self._tabela.insert(index, Line)

    def __str__(self):
        out = ''
        for line in self._tabela:
            out += "{:<8} {:<7} {:<6} {:<9} {:<8}\n".format(line[0],line[1],line[2],line[3],line[4])
        return out

class Line:
    def __init__(self, string: str):
        command, comment = '', ''
        if ';' in string:
            command, comment = string.split(';')
        else: command = string
        self.comment = comment
        line = command.split()
        if len(line) > 2:
            self.rotulo = line[0]
            self.mne = line[1]
            self.op = line[2]
        else:
            self.rotulo = ''
            self.mne = line[0]
            self.op = line[1]