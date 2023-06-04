
class Node:
    """
    Uma classe que representa um nó de uma árvore sintática.
    
    ...

    Atributos
    ---------
    symbol : str
        Símbolo do nó.

    n: list
        Lista(Utilizada para ponteiro) com o número de símbolos não operacionais encontrados.
    
    left_child : Node
        Nó filho á esquerda. 
        
    right_child : Node
        Nó filho á direita. 
    
    nullable: Boolean
        Identifica se nó é anulável.
    
    firstpos: List
        Firstpos do nó.
    
    lastpos: List
        Lastpos do nó.
        
    Métodos
    -------
    isNullable() -> Boolean:
        Retorna se no é nullable ou não.
        
    getLastpos() -> List:
        Retorna lastpos.
    
    getFirstpos() -> List:
        Retorna firstpos.
        
    getLeftChild() -> Node:
        Retorna nó filho á esquerda. 
        
    getRightChild() -> Node:
        Retorna nó filho á direita. 
    
    checkNullable() -> Boolean:
        Identifica se nó é nullable.
    
    calculateLastpos() -> List:
        Calcula lastpos.
    
    calculateFirstpos() -> List:
        Calcula firspos.
    
    followpos(followpos: dict) -> None:
        Calcula followpos em um nó.
        
    calculateFollowpos(followpos: dict) -> None:
        Calcula todos os followpos.
        
    print() -> None:
        Imprime árvore a partir de um nó.
    """
    def __init__(self, symbol: str, n=None, left_child=None, right_child=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.nullable = self.checkNullable() 
        if n != None and not self.nullable: 
            self.firstpos = [n[0]]
            self.lastpos = [n[0]]
            n[0] += 1
        else:
            self.firstpos = self.calculateFirstpos()
            self.lastpos = self.calculateLastpos()
        
    def isNullable(self):
        return self.nullable
    
    def getLastpos(self):
        return self.lastpos
    
    def getFirstpos(self):
        return self.firstpos
    
    def getLeftChild(self):
        return self.left_child
    
    def getRightChild(self):
        return self.right_child
    
    def checkNullable(self):
        if self.symbol == '&' or self.symbol == '*':
            return True
        elif self.symbol == '|':
            return self.left_child.isNullable()  or self.right_child.isNullable()
        elif self.symbol == '.':
            return self.left_child.isNullable()  and self.right_child.isNullable()
        else:
            return False

    def calculateLastpos(self):
        # Calcula lastpos
        if self.symbol == '|':
            return sorted(list(set(self.left_child.getLastpos()) | set(self.right_child.getLastpos())))
        elif self.symbol == '.':
            if self.right_child.isNullable():
                return sorted(list(set(self.left_child.getLastpos()) | set(self.right_child.getLastpos())))
            else:
                return self.right_child.getLastpos()
        elif self.symbol == '*':
            return self.left_child.getLastpos()
        else:
            return []
        
    def calculateFirstpos(self):
        # Calcula firstpos
        if self.symbol == '|':
            return sorted(list(set(self.left_child.getFirstpos()) | set(self.right_child.getFirstpos())))
        elif self.symbol == '.':
            if self.left_child.isNullable():
                return sorted(list(set(self.left_child.getFirstpos()) | set(self.right_child.getFirstpos())))
            else:
                return self.left_child.getFirstpos()
        elif self.symbol == '*':
            return self.left_child.getFirstpos()
        else:
            return []
 
    def followpos(self, followpos: dict):
        if self.symbol == '*':
            firstpos = self.firstpos
            lastpos = self.lastpos
            for l in lastpos:
                followpos[l] = sorted(list(set(followpos[l]) | set(firstpos)))
        
        if self.symbol == '.':
            firstpos = self.right_child.getFirstpos()
            lastpos = self.left_child.getLastpos()
            for l in lastpos:
                followpos[l] = sorted(list(set(followpos[l]) | set(firstpos)))
            
    def calculateFollowpos(self, followpos: dict):
        if self.left_child == None and self.right_child == None:
            return
        elif self.left_child == None:
            self.right_child.calculateFollowpos(followpos)
            return 
        elif self.right_child == None:
            self.left_child.calculateFollowpos(followpos)
            self.followpos(followpos)
            return
        else:
            self.left_child.calculateFollowpos(followpos)
            self.right_child.calculateFollowpos(followpos)
            self.followpos(followpos)
            return

    def print(self):
        if self.left_child == None and self.right_child == None:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos})"
        elif self.left_child == None or self.right_child == None:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos}) > ({self.left_child.print()})"
        else:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos}) > ({self.left_child.print()}, {self.right_child.print()})"


