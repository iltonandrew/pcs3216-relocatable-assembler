from typing import Generic, List,TypeVar
T = TypeVar("T")

class Symbol:
    def __init__(self, name: str,  symbolType: str):
        self._name = name
        self.address = None
        self._type = symbolType
        self.defined = False
        self._referenced = False

    def define(self):
        self.defined = True
    
    def __str__(self):
        return self._name + "   " + self.address + "   " + ('D' if self.defined else 'I') + "   " + self._type
    
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
                name:str,
                mnemonic: str,
                codeStruct: str,
                mneType: str,
                value: str,
                operand: str):
        self._mnemonic = mnemonic.strip()
        self._codeStruct = codeStruct.strip()
        self._type = mneType.strip()
        self._value = value.strip()
        self._operand = operand.strip()
        self._name = name.strip()

    def __str__(self):
        return self._codeStruct + "   " + self._type + "   " + self._mnemonic + "   " + self._name + "   " + self._value + "   " + self._operand

    def size(self):
        return len(self._codeStruct)//8
    def __eq__(self, other):
       if other == self._mnemonic:
           return True
       return False
    
    def key(self):
        return self._mnemonic;
    
    def __hash__(self):
        return hash(self._mnemonic)

class Table(Generic[T]):

    def __init__(self,  genericList: List[T]):
        self._dict = {}
        for item in genericList:
            self._dict[item.key()] = item
        
    def get(self, key: str):
        try:
            return self._dict[key]
        except KeyError:
            return None
    
    def set(self, item: T,):
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
    