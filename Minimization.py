from structures.AF import AF


class Minimization():
    """
    Uma classe para minimizar um AFD
    
    Métodos
    -------
    
    removeUnobtainables(af: AF) -> AF:
        Retorna  AFD sem estados inalcançáveis.
        
    removeDeadStates(af: AF) -> AF
        Retorna AFD sem estados mortos.
        
    removeEquivalents(af: AF) -> AF:
        Retorna AFD sem estados equivalentes.
    """
    
    
    def removeUnobtainables(af : AF):
        #AUTÔMATO INICIAL
        states = af.getStates()
        initial_state = af.getInitialState()
        symbols = af.getSymbols()
        final_states = af.getFinalStates()
        transitions = af.getTransitions()
        
        #Define lista para armazenar estados alcançáveis.
        attainable = []
        
        #Lista de estados encontrados.
        states_found = [initial_state]
        
        #Enquanto a lista de estados encontrados não estiver vazia.
        while len(states_found) != 0:
            #Pega e remove um estado da lista de estados encontrados.
            s = states_found.pop(0)
            
            #Se o estado ainda não estiver na lista de estados alcançáveis.
            if s not in attainable:
                #Adiciona na lista de estados alcançáveis.
                attainable.append(s)
                
                #Busca estados alcançáveis a partir de 's' e adiciona na lista de estados encontrados.
                for symbol in symbols:
                    state = transitions[s][symbol]
                    if state != None:
                        states_found.append(state)
        
        #AUTÔMATO RESULTANTE.
        new_states = sorted(attainable) #Novos estados igual a lista de estados alcançáveis.
        new_final_states = sorted(list(set(attainable) & set(final_states))) #Novos estados finais igual a interseção de estados alcançáveis com estados finais do autômato inicial.
        
        #Novas transições igual a transições do autômato inicial - transições de estados inalcançáveis.
        new_transitions = transitions 
        for a in sorted(list(set(states) - set(attainable))):
            new_transitions.pop(a)
        
        #Retorna autômato resultante.
        return AF(0, new_states, initial_state, symbols, new_final_states, new_transitions)
        

    def removeDeadStates(af: AF):
        #AUTÔMATO INICIAL
        states = af.getStates()
        initial_state = af.getInitialState()
        symbols = af.getSymbols()
        final_states = af.getFinalStates()
        transitions = af.getTransitions()
       
        #Define lista para armazenar estados não mortos.
        not_dead = []
        
        #Lista de estados encontrados.
        states_found = [] + final_states
        
        while len(states_found) != 0:
            #Pega e remove um estado da lista de estados encontrados.
            s = states_found.pop(0)
            
            #Se o estado ainda não estiver na lista de estados não mortos.
            if s not in not_dead:
                #Adiciona na lista de estados não mortos.
                not_dead.append(s)

                #Adiciona o estado que transita para 's' na lista de estados encontrados.
                for state in states:
                    for symbol in symbols:
                        if transitions[state][symbol] == s:
                            states_found.append(state)
        
        
        #AUTÔMATO RESULTANTE.
        new_states = sorted(not_dead) #Novos estados igual a lista de estados não mortos.
        
        #Novas transições igual a transições de estados não mortos. Se estado não morto transitar para estado morto, transição igual a None.
        new_transitions = {}
        
        for state in new_states:
            new_transitions[state] = {}
            for symbol in symbols:
                if transitions[state][symbol] in new_states:
                    new_transitions[state][symbol] = transitions[state][symbol]
                else:
                    new_transitions[state][symbol] = None
                    
        
        
        #Retorna autômato resultante.
        return AF(0, new_states, initial_state, symbols, final_states, new_transitions)
        
        

    def removeEquivalents(af: AF):
        #AUTÔMATO INICIAL
        states = af.getStates()
        initial_state = af.getInitialState()
        symbols = af.getSymbols()
        final_states = af.getFinalStates()
        transitions = af.getTransitions()
        
        #Lista de conjuntos de estados.
        sets = []
        #Nova lista de conjuntos de estados.
        new_sets = [final_states, sorted(list(set(states)-set(final_states)))] #Lista definida contendo conjunto de estados finais e conjunto de estados não finais.
        
        #Enquanto lista sets for diferente da lista new_sets.
        while len(sets) != len(new_sets):
            #Define sets como new_sets.
            sets = new_sets
            #Define new set como vazio.
            new_sets = []
            
            #Mapeia cada estado a partir de uma transição por um símbolo, para um conjunto em sets.
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
                            
            #Para cada estado em map_sets.       
            for state in map_sets:
                is_equivalent = False
                
                #Busca conjunto com estados que mapeiam para os mesmos conjunto por todos os símbolos em new_sets e os estados contidos neste conjunto partam do mesmo conjunto de 'state'.
                for s in new_sets:
                    for si in sets:
                        if map_sets[state] == map_sets[s[0]] and state in si and s[0] in si:
                            #Se encontrado, se agrupa no mesmo conjunto.
                            s.append(state)
                            is_equivalent = True
                            break
                        
                        if is_equivalent:
                            break
                        
                #Se não encontrar, cria um novo conjunto com o estado e adiciona em 'new_sets'.
                if not is_equivalent:
                    new_sets.append([state])
                    
                    
                
        #AUTÔMATO RESULTANTE.
        new_states = [str(state) for state in sets] #Define novos estados igual a lista de conjuntos.
        
        #Define o estado inicial, como conjunto que contém o estado inicial do autômato inicial.
        new_initial_state = None
        for state in sets:
            if initial_state in state:
                new_initial_state = str(state)
                break
            
        #Define estados finais, como conjuntos que contenham um estado final.
        new_final_states = []
        for state in sets:
            if len(list(set(state) & set(final_states))):
                new_final_states.append(str(state))
                
        #Define transições, de conjunto a partir de um símbolo para outro conjunto.
        new_transitions = {}
        for state in sets:
            new_transitions[str(state)] = {}
            for symbol in symbols:
                new_transitions[str(state)][symbol] = None
                for s in sets:
                    if transitions[state[0]][symbol] in s:
                        new_transitions[str(state)][symbol] = str(s)
                        
        
        
        #Retorna autômato resultante.
        return AF(0, new_states, new_initial_state, symbols, new_final_states, new_transitions)
