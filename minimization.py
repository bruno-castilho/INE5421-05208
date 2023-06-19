from structures.AF import AF


def removeUnobtainables(af : AF):
    states = af.getStates()
    initial_state = af.getInitialState()
    symbols = af.getSymbols()
    final_states = af.getFinalStates()
    transitions = af.getTransitions()
    
    attainable = []
    
    #Lista de estados encontrados.
    states_found = [initial_state]
    
    while len(states_found) != 0:
        #Pega um estado da lista.
        s = states_found.pop(0)
        
        if s not in attainable:
            #Adiciona na lista de estados alcançaveis.
            attainable.append(s)
            
            #Adiciona estados alcançaveis a partir de 's' e adiciona na lista de estados encontrados.
            for symbol in symbols:
                state = transitions[s][symbol]
                if state != None:
                    states_found.append(state)
    
    new_states = sorted(attainable)
    new_final_states = sorted(list(set(attainable) & set(final_states)))
    new_transitions = transitions
    
    for a in sorted(list(set(states) - set(attainable))):
        new_transitions.pop(a)
    
    return AF(0, new_states, initial_state, symbols, new_final_states, new_transitions)
    

def removeDeadStates(af: AF):
    states = af.getStates()
    initial_state = af.getInitialState()
    symbols = af.getSymbols()
    final_states = af.getFinalStates()
    transitions = af.getTransitions()
    
    not_dead = []
    
    #Lista de estados encontrados.
    states_found = [] + final_states
    
    while len(states_found) != 0:
        #Pega um estado da lista.
        s = states_found.pop(0)
        
        if s not in not_dead:
            #Adiciona na lista de estados não mortos.
            not_dead.append(s)

            #Adiciona cabeça de produção que contem 's' em sua produção em lista de estados encontrados.
            for state in states:
                for symbol in symbols:
                    if transitions[state][symbol] == s:
                        states_found.append(state)
    
    new_states = sorted(not_dead)
    new_transitions = {}
    
    for state in new_states:
        new_transitions[state] = {}
        for symbol in symbols:
            if transitions[state][symbol] in new_states:
                new_transitions[state][symbol] = transitions[state][symbol]
            else:
                new_transitions[state][symbol] = None
                
    
    
    
    return AF(0, new_states, initial_state, symbols, final_states, new_transitions)
    
    

def removeEquivalents(af: AF):
    states = af.getStates()
    initial_state = af.getInitialState()
    symbols = af.getSymbols()
    final_states = af.getFinalStates()
    transitions = af.getTransitions()
    
    sets = []
    new_sets = [final_states, sorted(list(set(states)-set(final_states)))]
    
    while len(sets) != len(new_sets):
        sets = new_sets
        new_sets = []
        
        map_sets = {}
        for state in states:
            map_sets[state] = {}
            for symbol in symbols:
                if transitions[state][symbol] == None:
                    map_sets[state][symbol] = None
                else:
                    for s in sets :
                        if transitions[state][symbol] in s:
                            map_sets[state][symbol] = s
                            break
                        
        for state in map_sets:
            check = False
            for s in new_sets:
                for si in sets:
                    if map_sets[state] == map_sets[s[0]] and state in si and s[0] in si:
                        s.append(state)
                        check = True
                        break
                    
                    if check:
                        break
                
            if not check:
                new_sets.append([state])
            

    #Define novos estados.
    new_states = [str(state) for state in sets]
    
    #Define estado inicial.
    new_initial_state = None
    for state in sets:
        if initial_state in state:
            new_initial_state = str(state)
            break
        
    #Define estados finais.
    new_final_states = []
    for state in sets:
        if len(list(set(state) & set(final_states))):
            new_final_states.append(str(state))
            
    #Define transições.
    new_transitions = {}
    for state in sets:
        new_transitions[str(state)] = {}
        for symbol in symbols:
            new_transitions[str(state)][symbol] = None
            for s in sets:
                if transitions[state[0]][symbol] in s:
                    new_transitions[str(state)][symbol] = str(s)
                    
    
    
    
    return AF(0, new_states, new_initial_state, symbols, new_final_states, new_transitions)

    
    


af = AF(type=0, 
        states=["[S']", "[A]","[A,C]","[C]","[S,X]","[D,X]","[E,X]"], 
        initial_state="[S']", 
        symbols=['a', 'b','c'], 
        final_states=["[S']", "[S,X]","[D,X]","[E,X]"],
        transitions= { 
                        "[S']": {
                            'a': "[A]",
                            'b': "[A,C]",
                            'c': "[C]"
                            },
                        "[A]": {
                            'a': None,
                            'b': "[S,X]",
                            'c': "[D,X]"
                            },
                        "[A,C]": {
                            'a': "[E,X]",
                            'b': "[S,X]",
                            'c': "[D,X]"
                            },
                        "[C]": {
                            'a': "[E,X]",
                            'b': "[S,X]",
                            'c': None
                            },
                        "[S,X]": {
                            'a': "[A]",
                            'b': "[A,C]",
                            'c': "[C]"
                            },
                        
                        "[D,X]": {
                            'a': "[A]",
                            'b': "[A,C]",
                            'c': None
                            },
                        
                        "[E,X]": {
                            'a': None,
                            'b': "[A,C]",
                            'c': "[C]"
                        }
                        }
        )

af.print()
af1 = removeUnobtainables(af)
af1.print()
af2 = removeDeadStates(af1)
af2.print()
removeEquivalents(af2).print()