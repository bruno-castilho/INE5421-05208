
class GR():
    def __init__(self, N, T, P, S):
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
            
            

