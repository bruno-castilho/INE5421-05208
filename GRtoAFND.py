from structures.AF import AF
from structures.GR import GR

class GRtoAFND():
    """
    Uma classe para transformar GR em AFND.
    
    Métodos
    -------
    
    transform(GR: GR) -> AF:
        Retorna AFND.
        
    """
    def transform(GR: GR):
        N = GR.getN()  
        T = GR.getT()
        if '&' in T:
            T.remove('&')
        P = GR.getP()
        S = GR.getS()
        
        transitions = {}
        
        for n in N:
            transitions[n] = {}
            
            for t in T:
                transitions[n][t] = []
                
            for p in P[n]:
                if p['t'] != '&':
                    if 'n' in p.keys():
                        transitions[n][p['t']] += [p['n']]
                    else:
                        transitions[n][p['t']] += ['X']
        
        transitions['X'] = {t: [] for t in T}
        
        states = N + ['X']  
        initial_state =  S
        symbols = T
        final_states = ['X']
        
        if '&' in [p['t'] for p in P[S]]:
            final_states.append(S)
        
        return AF(1,states, initial_state, symbols, final_states, transitions)
                 
