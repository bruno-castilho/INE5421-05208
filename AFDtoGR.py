from structures.AF import AF
from structures.GR import GR

def AFDtoGR(AF: AF):
    states = AF.getStates()
    initial_state = AF.getInitialState()
    symbols = AF.getSymbols()
    final_states = AF.getFinalStates()
    transitions = AF.getTransitions()
    
    P = {}
    for state in states:
        P[state] = []
        for symbol in symbols:
            if transitions[state][symbol]:
                P[state].append({'t': symbol, 'n': transitions[state][symbol]})
                if transitions[state][symbol] in final_states:
                    P[state].append({'t': symbol})
    
    if initial_state in final_states:
        P[initial_state].append({'t':'&'})
    
    N = states
    T = symbols
    S = initial_state
    return GR(N,T,P,S)
    
    
af = AF(states=['S','A', 'B', 'C'], 
        initial_state='S', 
        symbols=['a', 'b', 'c'], 
        final_states=['C'],
        transitions= { 
                        'S': {
                            'a': 'A',
                            'b': 'A',
                            'c': 'B'
                            },
                        'A': {
                            'a': 'S',
                            'b': 'S',
                            'c': 'C'
                        },
                        'B': {
                            'a': 'C',
                            'b': 'C',
                            'c': 'S'
                        },
                        'C': {
                            'a': 'B',
                            'b': 'B',
                            'c': 'A'
                        }
                        }
        )
af.print()
gr = AFDtoGR(af)
gr.print()