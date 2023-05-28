from structures.AF import AF
from structures.GR import GR

class Read():
    
    def AF(filename):
        ref_arquivo = open(f'data/{filename}', "r")
        type = ref_arquivo.readline().rstrip('\n')
        initial_state = ref_arquivo.readline().rstrip('\n')
        final_states = ref_arquivo.readline().rstrip('\n').split(',')
        symbols = ref_arquivo.readline().rstrip('\n').split(',')
        states = ref_arquivo.readline().rstrip('\n').split(',')        
        transitions = {}
            
        for state in states:
            transitions[state] = {}
            for symbol in symbols:
                if type == '0':
                    transitions[state][symbol] = None
                if type == '1':
                    transitions[state][symbol] = []
        
        for value in ref_arquivo:
            value = value.rstrip('\n').split(',')
            if type == '0':
                transitions[value[0]][value[1]] = value[2]
            if type == '1':
                transitions[value[0]][value[1]] = value[2].split('-')
        
        ref_arquivo.close()
        
        return AF(type, states, initial_state, symbols, final_states, transitions)
        

    
    def GRR(filename):
        ref_arquivo = open(f'data/{filename}', "r")
        N = ref_arquivo.readline().rstrip('\n').split(',')
        T = ref_arquivo.readline().rstrip('\n').split(',')
        S = ref_arquivo.readline().rstrip('\n') 
        P = {}
        
        for value in ref_arquivo:
            string = value.rstrip('\n') 
            string = string.replace(' ', '')
            list = string.split('->')
            H = list[0]
            P[H] = []
            for p in list[1].split('|'):
                for t in T:
                    if t in p:
                        data = {'t':t}
                        p = p.replace(t,'')
                        if len(p) > 0:
                            data['n'] = p
                            
                        P[H].append(data)
                        break
                    
        ref_arquivo.close()
        return GR(N=N,T=T,S=S,P=P)
        
        
        
        

