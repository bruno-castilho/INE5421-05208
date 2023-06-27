
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
    
    calculateFollowpos(followpos: dict) -> None:
        Calcula followpos em um nó.
        
    followpos(followpos: dict) -> None:
        #Percorre a árvore em profundidade, fazendo o cálculo de todos os Followpos.
        
    print() -> None:
        Imprime árvore a partir de um nó.
    """
    def __init__(self, symbol: str, n=None, left_child=None, right_child=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        
        #Verifica se nó é anulável.
        self.nullable = self.checkNullable() 
        
        #Se nó for folha e não anulável.
        if n != None and not self.nullable:
            #Firstpost e Lastpos igual uma lista contendo N. 
            self.firstpos = [n[0]]
            self.lastpos = [n[0]]
            #N += 1 para próximo nó folha.
            n[0] += 1
            
        #Se não, calcula Firstpos e Lastpos(se não for símbolo operando ambos serão uma lista vazia, ou seja se for '&' será vazio).
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
        #Se nó for '&' ou '*'.
        if self.symbol == '&' or self.symbol == '*':
            #É anulável.
            return True
        #Se nó for '|'.
        elif self.symbol == '|':
            #Se filho esquerdo ou direito for anulável, nó é anulável.
            return self.left_child.isNullable()  or self.right_child.isNullable()
        
        #Se nó for '.'.
        elif self.symbol == '.':
            #Se filho esquerdo e direito forem anuláveis, nó é anulável.
            return self.left_child.isNullable()  and self.right_child.isNullable()
        #Se não.
        else:
            #Não é anulável.
            return False

    def calculateLastpos(self): 
        #Se nó for operando 'ou'.
        if self.symbol == '|':
            #Lastpos igual a União de Lastpos dos filhos.
            return sorted(list(set(self.left_child.getLastpos()) | set(self.right_child.getLastpos())))

        #Se nó for operando 'concatenação'.
        elif self.symbol == '.':
            #Se filho direito for anulavel.
            if self.right_child.isNullable():
                #Lastpos igual a União de Lastpos dos filhos.
                return sorted(list(set(self.left_child.getLastpos()) | set(self.right_child.getLastpos())))
            else:
                #Lastpos igual a Lastpos do filho direito.
                return self.right_child.getLastpos()
                 
        #Se nó for operando 'fecho'.
        elif self.symbol == '*':
            #Lastpos igual a Lastpos do filho esquerdo(único).
            return self.left_child.getLastpos()
        #Se não
        else:
            #Retorna vazio.
            return []
        
    def calculateFirstpos(self):
        #Se nó for operando 'ou'.
        if self.symbol == '|':
            #Firstpos igual a União de Firstpos dos filhos.
            return sorted(list(set(self.left_child.getFirstpos()) | set(self.right_child.getFirstpos())))
        
        #Se nó for operando 'concatenação'.
        elif self.symbol == '.':
            if self.left_child.isNullable():
                #Firstpos igual a União de Firstpos dos filhos.
                return sorted(list(set(self.left_child.getFirstpos()) | set(self.right_child.getFirstpos())))
            else:
                #Firstpost igual a Firstpost do filho esquerdo.
                return self.left_child.getFirstpos()
        
        #Se nó for operando 'fecho'.
        elif self.symbol == '*':
            #Firstpos igual a Firstpos do filho esquerdo(único).
            return self.left_child.getFirstpos()
        
        #Se não
        else:
            #Retorna vazio.
            return []
 
    def calculateFollowpos(self, followpos: dict):
        #Se nó for 'fecho'
        if self.symbol == '*':
            #Fistpos do nó está em todos os Followpos dos Lastpos do nó.
            firstpos = self.firstpos
            lastpos = self.lastpos
            for l in lastpos:
                followpos[l] = sorted(list(set(followpos[l]) | set(firstpos)))
        
        #Se nó for 'concatenação'.
        if self.symbol == '.':
            #Firstpos do filho direito do nó estão nos Followpos dos Lastpos do filho esquerdo do nó.
            firstpos = self.right_child.getFirstpos()
            lastpos = self.left_child.getLastpos()
            for l in lastpos:
                followpos[l] = sorted(list(set(followpos[l]) | set(firstpos)))
            
    def followpos(self, followpos: dict):
        #Percorre a árvore em profundidade, fazendo o cálculo de todos os Followpos.
        if self.left_child == None and self.right_child == None:
            return
        elif self.left_child == None:
            self.right_child.followpos(followpos)
            return 
        elif self.right_child == None:
            self.left_child.followpos(followpos)
            self.calculateFollowpos(followpos)
            return
        else:
            self.left_child.followpos(followpos)
            self.right_child.followpos(followpos)
            self.calculateFollowpos(followpos)
            return

    def print(self):
        if self.left_child == None and self.right_child == None:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos})"
        elif self.left_child == None or self.right_child == None:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos}) > ({self.left_child.print()})"
        else:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos}) > ({self.left_child.print()}, {self.right_child.print()})"


