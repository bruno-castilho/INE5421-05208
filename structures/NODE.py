class NODE:
    def __init__(self, symbol, n=None, left_child=None, right_child=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.nullable = self.checkNullable() 
        if n != None and not self.nullable: 
            self.firstpos = [n[0]]
            self.lastpos = [n[0]]
            n[0] += 1
        else:
            self.firstpos = self.calcula_firstpos(n)
            self.lastpos = self.calcula_lastpos(n)
        
    def visualizar(self):
        if self.left_child == None and self.right_child == None:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos})"
        elif self.left_child == None or self.right_child == None:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos}) > ({self.left_child.visualizar()})"
        else:
            return f"{self.symbol}({self.nullable})({self.firstpos})({self.lastpos}) > ({self.left_child.visualizar()}, {self.right_child.visualizar()})"

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
        # Calcula nulos
        if self.symbol == '&' or self.symbol == '*':
            return True
        elif self.symbol == '|':
            return self.left_child.isNullable()  or self.right_child.isNullable()
        elif self.symbol == '.':
            return self.left_child.isNullable()  and self.right_child.isNullable()
        else:
            return False

    def calcula_lastpos(self, n):
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
        
    def calcula_firstpos(self, n):
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
 
    def followpos(self, followpos):
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
            
    def calcule_followpos(self, followpos):
        if self.left_child == None and self.right_child == None:
            return
        elif self.left_child == None:
            self.right_child.calcule_followpos(followpos)
            return 
        elif self.right_child == None:
            self.left_child.calcule_followpos(followpos)
            self.followpos(followpos)
            return
        else:
            self.left_child.calcule_followpos(followpos)
            self.right_child.calcule_followpos(followpos)
            self.followpos(followpos)
            return




