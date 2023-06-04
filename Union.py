from structures.AF import AF

class Union():
    """
    Uma classe para unir dois AFD.
    
    Métodos
    -------

    transform(AF1: AF, AF2: AF) -> AF
        Retorna AFND
    
    """
    
    def transform(AF1: AF, AF2: AF):        
        #AF1
        AF1.adjust('s')
        af1_states = AF1.getStates()
        af1_initial_state = AF1.getInitialState()
        af1_symbols = AF1.getSymbols()
        af1_final_states = AF1.getFinalStates()
        af1_transitions = AF1.getTransitions()
        
        #AF2
        AF2.adjust('t')
        af2_states = AF2.getStates()
        af2_initial_state = AF2.getInitialState()
        af2_symbols = AF2.getSymbols()
        af2_final_states = AF2.getFinalStates()
        af2_transitions = AF2.getTransitions()
        
        #Novo AF
        new_initial_state = 'i0'
        new_states = [new_initial_state] + af1_states + af2_states 
        new_symbols = sorted(list(set(af1_symbols) | set(af2_symbols) | set(['&'])))
        new_final_states = af1_final_states + af2_final_states
        new_transitions = {}
        
        for state in new_states:
            new_transitions[state] = {}
            for symbol in new_symbols:
                new_transitions[state][symbol] = []
                
        new_transitions[new_initial_state]['&'] = [af1_initial_state, af2_initial_state]
        
        for state in af1_states:
            for symbol in af1_symbols:
                if af1_transitions[state][symbol]:
                    new_transitions[state][symbol] = [af1_transitions[state][symbol]]
                else:
                    new_transitions[state][symbol] = []
        
        for state in af2_states:
            for symbol in af2_symbols:
                if af2_transitions[state][symbol]:
                    new_transitions[state][symbol] = [af2_transitions[state][symbol]]
                else:
                    new_transitions[state][symbol] = []
                    
        return AF(1, new_states, new_initial_state, new_symbols, new_final_states, new_transitions)