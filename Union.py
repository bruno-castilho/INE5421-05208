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
        #AF1.
        AF1.adjust('s')
        af1_states = AF1.getStates()
        af1_initial_state = AF1.getInitialState()
        af1_symbols = AF1.getSymbols()
        af1_final_states = AF1.getFinalStates()
        af1_transitions = AF1.getTransitions()
        
        #AF2.
        AF2.adjust('t')
        af2_states = AF2.getStates()
        af2_initial_state = AF2.getInitialState()
        af2_symbols = AF2.getSymbols()
        af2_final_states = AF2.getFinalStates()
        af2_transitions = AF2.getTransitions()
        
        #NOVO AFND.
        new_initial_state = 'i0' #Estado inicial do autômato igual a 'i0'.
        new_states = [new_initial_state] + af1_states + af2_states #Lista de estados do autómato igual a 'i0' + estados do AF1 + estados do AF2.
        new_symbols = sorted(list(set(af1_symbols) | set(af2_symbols) | set(['&']))) #Lista de símbolos igual a união de símbolos de AF1 e AF2.
        new_final_states = af1_final_states + af2_final_states #Lista de estados finais igual a estados finais de AF1 e AF2.
        
        #Define transições.
        new_transitions = {}
        
        #Para cada estado sem 's'.
        for state in new_states:
            #Cria-se transições vazias para cada símbolo.
            new_transitions[state] = {}
            for symbol in new_symbols:
                new_transitions[state][symbol] = []
        
        #Define uma transição partindo de 'i0' por '&' para os estados iniciais de AF1 e AF2.     
        new_transitions[new_initial_state]['&'] = [af1_initial_state, af2_initial_state]
        
        #Define transições do novo automato igual a transições de AF1 e AF2.
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
        
        #Retorna autômato resultante.   
        return AF(1, new_states, new_initial_state, new_symbols, new_final_states, new_transitions)