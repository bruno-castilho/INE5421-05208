from structures.AF import AF
from structures.GR import GR

def GRtoAFND(GR: GR):
    N = GR.getN()  
    T = GR.getT()
    P = GR.getP()
    S = GR.getS()
    
    transitions = {}
    
    for n in N:
        transitions[n] = {}
        
        for t in T:
            transitions[n][t] = []
            
        for p in P[n]:
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
    
    return AF(states, initial_state, symbols, final_states, transitions)
                 
gr = GR(N=["S'",'S','A','C','D','E'], T=['a','b','c','&'], S="S'", P={
    "S'": [{'t':'a', 'n':'A'}, {'t':'c', 'n':'C'}, {'t':'b', 'n':'A'},{'t':'b', 'n':'C'}, {'t': '&'}],
    'S': [{'t':'a', 'n':'A'},{'t':'c','n':'C'},{'t':'b','n':'A' },{'t':'b','n':'C'}],
    'A': [{'t':'b','n':'S'},{'t':'c','n':'D'},{'t':'b'},{'t':'c'}],
    'C': [{'t':'b','n':'S'},{'t':'a','n':'E'},{'t':'b'},{'t':'a'}],
    'D': [{'t':'a', 'n':'A'},{'t':'b','n':'A'},{'t':'b','n':'C'}],
    'E': [{'t':'c','n':'C'},{'t':'b','n':'C'},{'t':'b','n':'A'}],
})
gr.print()
GRtoAFND(gr).print()