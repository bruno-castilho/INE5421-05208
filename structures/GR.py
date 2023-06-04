
class GR():
    """
    Uma classe para representar uma Gramática Regular.
    
    ...

    Atributos
    ---------
    N : List
        Lista de não terminais.
        
    T : List
        Lista de terminais.
    
    P : Dict
        Dicionário que mapeia produções de cada não terminal.
    
    S : Str
        Símbolo inicial da gramática.
        
    Métodos
    -------
    getN() -> List:
        Retorna lista de não terminais.
        
    getT() -> List:
        Retorna lista de terminais.
        
    getP() -> Dict:
        Retorna dicionário que mapeia produções de cada não terminal.
        
    getS() -> Str:
        Retorna símbolo inicial da gramática.
    
    print() -> None:
        Imprime a gramática.
    """
    def __init__(self, N: list, T: list, P: dict, S: str):
        self.N = N
        self.T = T
        self.P = P
        self.S = S
    
    def getN(self):
        return self.N
    
    def getT(self):
        return self.T
    
    def getP(self):
        return self.P
    
    def getS(self):
        return self.S
    
    def print(self):
        for n in self.N:
            str = n + '-> '
            for p in self.P[n]:
                str += p['t']
                if 'n' in p.keys():
                    str += p['n']
                
                str += ' | '
                
            print(str[0:-2])
            
            

